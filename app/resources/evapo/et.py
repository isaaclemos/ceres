from math import *
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
elev_rad = ((elev_sun/180)*pi)

# Alguns paramentrosdo vis e ivp

lmin_vis = -1.17
lmax_vis = 264
esun_vis = 1556.5
lmin_ivp = -1.51
lmax_ivp = 221
esun_ivp = 1050.5

# calculos do visivel


lman_vis = lmax_vis*cos(elev_rad)
lmin_vis_z = lmin_vis*cos(elev_rad)
dif_lmax_lmin_vis = lman_vis - lmin_vis_z
ganho_vis = dif_lmax_lmin_vis/(vis_max-vis_min)
offset_vis = lmin_vis_z
coef_vis = (pi*dist_terra_sol*dist_terra_sol)/((esun_vis)*cos(elev_rad))
coef_albedo_vis = dif_lmax_lmin_vis/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))

# calculos da infraviselho proximo


lman_ivp = lmax_ivp*cos(elev_rad)
lmin_ivp_z = lmin_ivp*cos(elev_rad)
dif_lmax_lmin_ivp = lman_ivp-lmin_ivp_z
ganho_ivp = dif_lmax_lmin_ivp/(ivp_max-ivp_min)
offset_ivp = lmin_ivp_z
coef_ivp = (pi*dist_terra_sol*dist_terra_sol)/((esun_ivp)*cos(elev_rad))
coef_albedo_ivp = dif_lmax_lmin_ivp/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))

def vis_rad(vis_band3):
    return (vis_band3*ganho_vis)+offset_vis


def ivp_rad(ivp_band1):
    return (ivp_band1*ganho_ivp)+offset_ivp


def vis_reflect(vis_rad):
    return vis_rad*coef_vis


def ivp_reflec(ivp_rad):
    return ivp_rad*coef_ivp


def NDVI(vis_reflect, ivp_reflect):
    return (ivp_reflect-vis_reflect)/(ivp_reflect+vis_reflect)


def TRANSMITIVIDADE_ATM(NDVI):
    # Rever 2E pois não me lembro
    return (0.75 + (2E-5*(NDVI/NDVI)*altitude))


def EMISSIVIDADE_ATM(TRANSMITIVIDADE_ATM):
    # Rever Logaritimo natural em python math.log()
    return (0.85*((-1*(log(TRANSMITIVIDADE_ATM))) ^ 0.09))


def lin(EMISSIVIDADE_ATM):
    # Rever exponencial (5.6e) em python esta correto
    return (EMISSIVIDADE_ATM*(exp(5.67)-8)*(temp ^ 4))


def EMISSIVIDADE_VEG(NDVI):
    return (NDVI >= 0.24)*((1.0094)+(0.10824*log10(NDVI)))


def EMISSIVIDADE_SOLO(NDVI):
    return (NDVI < 0.24)*0.94


def TEMP_VEG(NDVI):
    # Rever a utilação da temperatura, pois a mascara deve servir
    # para a utiliação dos dados termais
    return ((NDVI >= 0.24)*1)*temp


def TEMP_SOLO(NDVI):
    # Idem a função anterior
    return ((NDVI < 0.24)*1)*temp


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
media_veg = 0
media_solo = 0
fr = 0


def LOUTC(EMISSIVIDADE_VEG, NDVI):
    # Rever 5.67e
    return (((NDVI >= 0.24)*(media_veg ^ 4))*EMISSIVIDADE_VEG*exp(5.67)-8)


def LOUTS(EMISSIVIDADE_SOLO, NDVI):
    # Rever 5.67e
    return (((NDVI < 0.24)*(media_solo ^ 4))*EMISSIVIDADE_SOLO*exp(5.67)-8)


def RSE(TRANSMITIVIDADE_ATM):
    return (esun_sol*(dist_terra_sol)*(cos(elev_rad))*(TRANSMITIVIDADE_ATM))


def ALBEDO_VEG(VIS_REFLEC, IVP_REFLEC, NDVI):
    # Rever formula pois possivelmente esta errada
    return (NDVI >= 0.24)*((IVP_REFLEC*coef_albedo_ivp)+(IVP_REFLEC*coef_albedo_vis))


def ALBEDO_SOLO(VIS_REFLEC, IVP_REFLEC, NDVI):
    # Rever formula pois possivelmente esta errada
    return (NDVI < 0.24)*((IVP_REFLEC*coef_albedo_ivp)+(IVP_REFLEC*coef_albedo_vis))


def RNS(ALBEDO_VEG, RSE, LIN, LOUTC, EMISSIVIDADE_VEG):
    return ((1-ALBEDO_VEG)*RSE)+LIN-LOUTC-((1-EMISSIVIDADE_VEG)*LIN)


def RNS(ALBEDO_SOLO, RSE, LIN, LOUTS, EMISSIVIDADE_SOLO):
    return ((1-ALBEDO_SOLO)*RSE)+LIN-LOUTS-((1-EMISSIVIDADE_SOLO)*LIN)


def RNE(RNC, RNS):
    return fr*RNC+(1-fr)*RNS


def SAVI(IVP_REFLEC, VIS_REFLEC):
    return (1.5*(IVP_REFLEC-VIS_REFLEC))/(0.5+(IVP_REFLEC+VIS_REFLEC))


def IAF(SAVI):
    # Confirmar logaritimo natural ln em gdal
    return (-1*((log((0.69-SAVI)/0.59))/0.91))


def RAC(IAF):
    return (IAF >= 0.5)*(25/IAF)

# confirmar log10 como log() gdal


RAS0 = (log10(alt_referencia/(0.05*alt_dossel*0.1)))*(log10((0.63 * alt_dossel+(0.05*alt_dossel*0.1))/(0.05*alt_dossel*0.1)))/((vento*0.41)**2)
RAS1 = (((log10((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel*0.1)))/(vento*0.41)**2)*(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(exp(2.5)-exp(2.5*(1-((0.63*alt_dossel)+((0.05*alt_dossel*0.1)/alt_dossel)))))
RAA0 = (((log10(alt_referencia/(0.05*alt_dossel*0.1)))**2)/((vento*0.41)**2))-RAS0 
RAA1 = ((log10((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel)))/((vento*0.41)**2))*((log((alt_referencia-(0.63*alt_dossel))/(alt_dossel-(0.63*alt_dossel))))+(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(exp(2.5*(1-(((alt_dossel*0.63)+(0.05*alt_dossel))/alt_dossel)))-1)


def RAS(IAF):
    return ((IAF/10)*RAS1)+(((4-IAF)/10)*RAS0)


def RAA(IAF):
    return ((IAF/20)*RAA1)+(((4-IAF)/20)*RAA0)


def HC(RAA, RAC):
    return (1.15*1005*0.10)/(RAC+RAA)


def HC(RAA(), RAS()):
    return (1.15*1005*0.13)/(RAS+RAA)


def HE(HC=HC(), HS=HC(), NDVI=NDVI()):
    return fr*HC+(1-fr)*HS


def GE(RNE=RNE()):
    return (0.3236*RNE)-51.52

def LEE(RNE=RNE(),HE=HE(),GE=GE()):
    return RNE-HE-GE

def LAMBDA(EMISSIVIDADE_VEG,EMISSIVIDADE_SOLO):
    # Confirmar dados de temperatura e 1e6
    return ((2.501-0.00236*((temp*(EMISSIVIDADE_VEG+EMISSIVIDADE_SOLO))-273.16))*(1e6))
    

def ET (LEE=LEE(),LAMBDA=LAMBDA()):
    return (3600*LEE)/LAMBDA