import math
import rasterio

# Entrada de temperatura

temp = 0

# Entrada de vento

vento = 1

# entradas comum

elev_sun = 1
altitude = 637
dist_terra_sol = 1
alt_dossel = 2
alt_referencia = 2

# Entrada do visivel

vis_min = 0
vis_max = 255

# Entrada do Infra

ivp_min = 0
ivp_max = 255

# Criacao de variaveis e suas equacoes

# Converter elevacao solar de Graus para Radianos
esun_sol = 1367
elev_rad = ((elev_sun/180)*math.pi)

# Alguns paramentrosdo vis e ivp

lmin_vis = -1.17
lmax_vis = 264
esun_vis = 1556.5
lmin_ivp = -1.51
lmax_ivp = 221
esun_ivp = 1050.5

# calculos do visivel


lman_vis = lmax_vis*math.cos(elev_rad)
lmin_vis_z = lmin_vis*math.cos(elev_rad)
dif_lmax_lmin_vis = lman_vis - lmin_vis_z
ganho_vis = dif_lmax_lmin_vis/(vis_max-vis_min)
offset_vis = lmin_vis_z
coef_vis = (math.pi*dist_terra_sol*dist_terra_sol) / \
    ((esun_vis)*math.cos(elev_rad))
coef_albedo_vis = dif_lmax_lmin_vis/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))

# calculos da infraviselho proximo


lman_ivp = lmax_ivp*math.cos(elev_rad)
lmin_ivp_z = lmin_ivp*math.cos(elev_rad)
dif_lmax_lmin_ivp = lman_ivp-lmin_ivp_z
ganho_ivp = dif_lmax_lmin_ivp/(ivp_max-ivp_min)
offset_ivp = lmin_ivp_z
coef_ivp = (math.pi*dist_terra_sol*dist_terra_sol)/(esun_ivp*math.cos(elev_rad))
coef_albedo_ivp = dif_lmax_lmin_ivp/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))


def vis_rad(vis_band3):
    return (vis_band3*ganho_vis)+offset_vis


def ivp_rad(ivp_band1):
    return (ivp_band1*ganho_ivp)+offset_ivp


def vis_reflect(vis_rad):
    return vis_rad*coef_vis


def ivp_reflec(ivp_rad):
    return ivp_rad*coef_ivp


def ndvi(vis_reflect, ivp_reflect):
    return (ivp_reflect-vis_reflect)/(ivp_reflect+vis_reflect)


def transmitividade_atm(ndvi):
    # Rever 2E pois não me lembro
    return (0.75 + (2E-5*(ndvi/ndvi)*altitude))


def emissividade_atm(transmitividade_atm):
    # Rever Logaritimo natural em python math.log()
    return (0.85*((-1*(math.log(transmitividade_atm))) ^ 0.09))


def lin(emissividade_atm):
    # Rever exponencial (5.6e) em python esta correto
    return (emissividade_atm*(5.67e-8)*(temp^4))


def emissividade_veg(ndvi):
    return (ndvi >= 0.24)*(1.0094+(0.10824*math.log10(ndvi)))


def emissividade_solo(ndvi):
    return (ndvi < 0.24)*0.94


def temp_veg(ndvi):
    # Rever a utilação da temperatura, pois a mascara deve servir
    # para a utiliação dos dados termais
    return ((ndvi >= 0.24)*1)*temp


def temp_solo(ndvi):
    # Idem a função anterior
    return ((ndvi < 0.24)*1)*temp


# Estatisticas dos rasters

# Refazer tudo do zero
'''

provider1 = layer25.dataProvider()
ext1 = layer25.extent()
stats1 = provider1.bandStatistics(1,QgsRasterBandStats.All,ext1,0)

provider2 = layer26.dataProvider()
ext2 = layer26.extent()
stats2 = provider2.bandStatistics(1,QgsRasterBandStats.All,ext1,0)

media_veg = stats1.mean
media_solo = stats2.mean 

fr=(stats1.sum/stats1.maximumValue)/stats1.elementCount

'''
temp_v = temp_veg(ndvi())
temp_s=temp_solo(ndvi())
media_veg = temp_v.mean
media_solo = temp_s.mean
fr = (temp_v.sum/temp_v.max)/temp_v.count


def loutc(emissividade_veg, ndvi):
    return (((ndvi >= 0.24)*(media_veg^4))*emissividade_veg*5.67e-8)


def louts(emissividade_solo, ndvi):
    return (((ndvi < 0.24)*(media_solo ^ 4))*emissividade_solo*5.67e-8)


def rse(transmitividade_atm):
    return (esun_sol*(dist_terra_sol)*(math.cos(elev_rad))*(transmitividade_atm))


def albedo_veg(vis_reflec, ivp_reflec, ndvi):
    # Rever formula pois possivelmente esta errada
    return (ndvi >= 0.24)*((ivp_reflec*coef_albedo_ivp)+(ivp_reflec*coef_albedo_vis))


def albedo_solo(vis_reflec, ivp_reflec, ndvi):
    # Rever formula pois possivelmente esta errada
    return (ndvi < 0.24)*((ivp_reflec*coef_albedo_ivp)+(ivp_reflec*coef_albedo_vis))


def rnc(albedo_veg, rse, lin, loutc, emissividade_veg):
    return ((1-albedo_veg)*rse)+lin-loutc-((1-emissividade_veg)*lin)


def rns(albedo_solo, rse, lin, louts, emissividade_solo):
    return ((1-albedo_solo)*rse)+lin-louts-((1-emissividade_solo)*lin)


def rne(rnc, rns):
    return fr*rnc+(1-fr)*rns


def savi(ivp_reflec, vis_reflec):
    return (1.5*(ivp_reflec-vis_reflec))/(0.5+(ivp_reflec+vis_reflec))


def iaf(savi):
    return (-1*((math.log((0.69-savi)/0.59))/0.91))


def rac(iaf):
    return (iaf >= 0.5)*(25/iaf)


ras0 = (math.log10(alt_referencia/(0.05*alt_dossel*0.1)))*(math.log10((0.63 *
                                                             alt_dossel+(0.05*alt_dossel*0.1))/(0.05*alt_dossel*0.1)))/((vento*0.41)**2)
ras1 = (((math.log10((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel*0.1)))/(vento*0.41)**2)*(alt_dossel/(2.5 *
        (alt_dossel-(0.63*alt_dossel)))))*(math.exp(2.5)-math.exp(2.5*(1-((0.63*alt_dossel)+((0.05*alt_dossel*0.1)/alt_dossel)))))
raa0 = (((math.log10(alt_referencia/(0.05*alt_dossel*0.1)))**2)/((vento*0.41)**2))-ras0
raa1 = ((math.log10((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel)))/((vento*0.41)**2))*((math.log((alt_referencia-(0.63*alt_dossel))/(alt_dossel -
                                                                                                                                   (0.63*alt_dossel))))+(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(exp(2.5*(1-(((alt_dossel*0.63)+(0.05*alt_dossel))/alt_dossel)))-1)


def ras(iaf):
    return ((iaf/10)*ras1)+(((4-iaf)/10)*ras0)


def raa(iaf):
    return ((iaf/20)*raa1)+(((4-iaf)/20)*raa0)


def hc(raa, rac):
    return (1.15*1005*0.10)/(rac+raa)


def he(hc, HS, ndvi):
    return fr*hc+(1-fr)*HS


def ge(rne):
    return (0.3236*rne)-51.52


def lee(rne, he, ge):
    return rne-he-ge


def lambda_et(emissividade_veg, emissividade_solo):
    # Confirmar dados de temperatura e 1e6
    return ((2.501-0.00236*((temp*(emissividade_veg+emissividade_solo))-273.16))*(1e6))


def et(lee, lambda_et):
    return (3600*lee)/lambda_et
