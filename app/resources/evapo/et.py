import numpy as np
import rasterio

from ...models import Station

np.seterr(divide='ignore')

def two_source_model(image: str, vento:float, sun_values:dict, temp_kelvin:float, station:Station):        

    
    # Entrada da imagem vinda da estaçao
    vis_band3 = rasterio.open(image).read(3).astype('float64')
    ivp_band1 = rasterio.open(image).read(1).astype('float64')
    # Entrada da imagem vinda da estaçao

    # ------------------------------------------------------------------------------
    # Valores minimos e maximo das bandas vis e ivp

    vis_min = np.nanmin(vis_band3)
    vis_max = np.nanmax(vis_band3)
    ivp_min = np.nanmin(ivp_band1)
    ivp_max = np.nanmax(ivp_band1)

    # ------------------------------------------------------------------------------
    # Dados thermais do sensor

    temp = temp_kelvin
    # ------------------------------------------------------------------------------
    # Dados do INMET

    vento = vento
    # ------------------------------------------------------------------------------
    # Dados oriundos da estação de coleta de dados

    altitude =  float(station.altitude)
    alt_dossel = float(station.altura_dossel)
    alt_referencia = float(station.altura)
    # ------------------------------------------------------------------------------
    # Dados essencias do Sol
    elev_sun = sun_values['sun_elev']
    dist_terra_sol = sun_values['dist_earth_sun']
    esun_sol = 1367
    elev_rad = ((elev_sun/180)*np.pi)

    # ------------------------------------------------------------------------------
    # Parametros constantes do sensor do vis e ivp

    LMIN_VIS = -1.17
    LMAX_VIS = 264
    ESUN_VIS = 1556.5
    LMIN_IVP = -1.51
    LMAX_IVP = 221
    ESUN_IVP = 1050.5
    # ------------------------------------------------------------------------------
    # Obtenção dos parametros do visivel

    lman_vis = LMAX_VIS*np.cos(elev_rad)
    lmin_vis_z = LMIN_VIS*np.cos(elev_rad)
    dif_lmax_lmin_vis = lman_vis - lmin_vis_z
    ganho_vis = dif_lmax_lmin_vis/(vis_max-vis_min)
    offset_vis = lmin_vis_z
    coef_vis = (np.pi*dist_terra_sol*dist_terra_sol) / \
        ((ESUN_VIS)*np.cos(elev_rad))
    coef_albedo_vis = dif_lmax_lmin_vis / \
        ((LMAX_VIS+LMAX_IVP)-(LMIN_VIS+LMIN_IVP))
    # ------------------------------------------------------------------------------
    # Obtenção dos parametros do infravermelho proximo

    lman_ivp = LMAX_IVP*np.cos(elev_rad)
    lmin_ivp_z = LMIN_IVP*np.cos(elev_rad)
    dif_lmax_lmin_ivp = lman_ivp-lmin_ivp_z
    ganho_ivp = dif_lmax_lmin_ivp/(ivp_max-ivp_min)
    offset_ivp = lmin_ivp_z
    coef_ivp = (np.pi*dist_terra_sol*dist_terra_sol)/(ESUN_IVP*np.cos(elev_rad))
    coef_albedo_ivp = dif_lmax_lmin_ivp/((LMAX_VIS+LMAX_IVP)-(LMIN_VIS+LMIN_IVP))

    # Processamento necessario para conversão de contadores digitais para valores de
    # reflectância da imagem oriunda da estação

    vis_rad = (vis_band3*ganho_vis)+offset_vis
    ivp_rad = (ivp_band1*ganho_ivp)+offset_ivp
    vis_reflect = vis_rad*coef_vis
    ivp_reflect = ivp_rad*coef_ivp
    # --------------------------------------------------------------------------------
    # Indices de vegetação

    ndvi = (ivp_reflect-vis_reflect)/(ivp_reflect+vis_reflect)
    savi = (1.5*(ivp_reflect-vis_reflect))/(0.5+(ivp_reflect+vis_reflect))
    iaf = (-1*((np.log((0.69-savi)/0.59))/0.91))

    # Execução do modelo matemático Two source

    transmitividade_atm = (0.75 + (2e-5*altitude))
    emissividade_atm = (0.85*((-1*(np.log(transmitividade_atm)))**0.09))
    lin = (emissividade_atm*(5.67e-8)*(temp**4))

    emissividade_veg = (ndvi >= 0.24)*(1.0094+(0.10824*np.log10(ndvi)))
    emissividade_solo = (ndvi < 0.24)*0.94

    temp_veg = ((ndvi >= 0.24)*1)*temp
    temp_solo = ((ndvi < 0.24)*1)*temp

    # Estatisticas dos rasters
    media_veg = np.nanmean(temp_veg)
    media_solo = np.nanmean(temp_solo)
    fr = (np.nansum(temp_veg)/np.nanmax(temp_veg))/np.size(temp_veg)

    loutc = (((ndvi >= 0.24)*media_veg**4)*emissividade_veg*5.67e-8)
    louts = (((ndvi < 0.24)*(media_solo**4))*emissividade_solo*5.67e-8)
    rse = (esun_sol*(dist_terra_sol)*(np.cos(elev_rad))*(transmitividade_atm))
    # Rever formula pois possivelmente esta errada
    albedo_veg = (ndvi >= 0.24)*((ivp_reflect*coef_albedo_ivp)+(ivp_reflect*coef_albedo_vis))
    # Rever formula pois possivelmente esta errada
    albedo_solo = (ndvi < 0.24)*((ivp_reflect*coef_albedo_ivp)+(ivp_reflect*coef_albedo_vis))
    # rnc = radiação líquida estimada sobre o dossel
    rnc = ((1-albedo_veg)*rse)+lin-loutc-((1-emissividade_veg)*lin)
    # rnc = radiação líquida estimada sobre o solo
    rns = ((1-albedo_solo)*rse)+lin-louts-((1-emissividade_solo)*lin)
    # rne = radiação líquida estimada sobre a viticultura
    rne = fr*rnc+(1-fr)*rns
    rac = (iaf >= 0.5)*(25/iaf)
    ras0 = (np.log(alt_referencia/(0.05*alt_dossel*0.1)))*(np.log((0.63 *  alt_dossel+(0.05*alt_dossel*0.1))/(0.05*alt_dossel*0.1)))/((vento*0.41)**2)
    ras1 = (((np.log((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel*0.1)))/(vento*0.41)**2)*(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(np.exp(2.5)-np.exp(2.5*(1-((0.63*alt_dossel)+((0.05*alt_dossel*0.1)/alt_dossel)))))
    raa0 = (((np.log(alt_referencia/(0.05*alt_dossel*0.1)))**2)/((vento*0.41)**2))-ras0
    raa1 = ((np.log((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel)))/((vento*0.41)**2))*((np.log((alt_referencia-(0.63*alt_dossel))/(alt_dossel-(0.63*alt_dossel))))+(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(np.exp(2.5*(1-(((alt_dossel*0.63)+(0.05*alt_dossel))/alt_dossel)))-1)
    ras = ((iaf/10)*ras1)+(((4-iaf)/10)*ras0)
    raa = ((iaf/20)*raa1)+(((4-iaf)/20)*raa0)

    # hc = fluxo de calor sensível no dossel
    hc = (1.15*1005*0.10)/(rac+raa)

    # hs = fluxo de calor sensível superfície do solo
    hs = (1.15*1005*0.13)/(ras+raa)

    # he = fluxo de calor sensível acima do dossel
    he = fr*hc+(1-fr)*hs

    # ge = fluxo de calor estimado
    ge = (0.3236*rne)-51.52

    # lee = fluxo  de  calor  latente  sobre  o  dossel
    lee = rne-he-ge

    lambda_et = (
        (2.501-0.00236*((temp*(emissividade_veg+emissividade_solo))-273.16))*(1e6))
    # et = evapotranspiração horaria
    et = (3600*lee)/lambda_et

    return et
