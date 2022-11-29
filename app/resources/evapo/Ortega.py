##Raster=group
##Ortega=name 
##vis=raster
#vis_select=selection 0;1;2;3;4;5;6;7;8;9;10;11
##ivp=raster
#ivp_select=selection 0;1;2;3;4;5;6;7;8;9;10;11

#Entrada de temperatura

##temp=number 0

#Entrada de vento

##vento=number 0

#entradas comum 

##elev_sun=number 0
##altitude=number 637
##dist_terra_sol=number 0
##alt_dossel=number 0
##alt_referencia=number 0

#Entrada do visivel

##vis_min=number 0
##vis_max=number 255

#Entrada do Infra

##ivp_min=number 0
##ivp_max=number 255

#Raster de saidas
##VIS_RAD=output raster
##IVP_RAD=output raster
##VIS_REFLEC=output raster
##IVP_REFLEC=output raster
##NDVI=output raster
##SAVI=output raster
##IAF=output raster
##TRANSMITIVIDADE_ATM=output raster
##EMISSIVIDADE_ATM=output raster
##LIN=output raster
##TEMP_VEG=output raster
##TEMP_SOLO=output raster
##LOUTC=output raster
##LOUTS=output raster
##EMISSIVIDADE_VEG=output raster
##EMISSIVIDADE_SOLO=output raster
##RSE=output raster
##ALBEDO_VEG=output raster
##ALBEDO_SOLO=output raster
##RNC=output raster
##RNS=output raster
##RNE=output raster
##RAC=output raster
##RAS=output raster
##RAA=output raster
##HC=output raster
##HS=output raster
##HE=output raster
##GE=output raster
##LEE=output raster
##LAMBDA=output raster
##ET=output raster

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry 
from qgis.core import QgsRasterBandStats
from  math import * 

#Criacao de variaveis e suas equacoes

#Converter elevacao solar de Graus para Radianos
esun_sol = 1367
elev_rad = ((elev_sun/180)*pi)

#Alguns paramentrosdo vis e ivp

lmin_vis = -1.17
lmax_vis = 264
esun_vis = 1556.5
lmin_ivp = -1.51
lmax_ivp = 221
esun_ivp = 1050.5

#calculos do visivel


lman_vis = lmax_vis*cos(elev_rad)
lmin_vis_z=lmin_vis*cos(elev_rad)
dif_lmax_lmin_vis = lman_vis- lmin_vis_z
ganho_vis = dif_lmax_lmin_vis/(vis_max-vis_min)
offset_vis = lmin_vis_z
coef_vis = (pi*dist_terra_sol*dist_terra_sol)/((esun_vis)*cos(elev_rad))
coef_albedo_vis=dif_lmax_lmin_vis/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))

#calculos da infraviselho proximo


lman_ivp = lmax_ivp*cos(elev_rad)
lmin_ivp_z=lmin_ivp*cos(elev_rad)
dif_lmax_lmin_ivp = lman_ivp-lmin_ivp_z
ganho_ivp = dif_lmax_lmin_ivp/(ivp_max-ivp_min)
offset_ivp =lmin_ivp_z
coef_ivp = (pi*dist_terra_sol*dist_terra_sol)/((esun_ivp)*cos(elev_rad))
coef_albedo_ivp=dif_lmax_lmin_ivp/((lmax_vis+lmax_ivp)-(lmin_vis+lmin_ivp))

#Primeiro  transformar a camada em obejto 

layer1 = processing.getObject(vis)
layer2 = processing.getObject(ivp)

def mask (vis,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='vis@1'
   raster1.raster=vis
   raster1.bandNumber=3
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("vis@1"*%s)+(%s)'%(ganho_vis,offset_vis),output,'GTiff',vis.extent(),vis.width(),vis.height(),entries)
   calc.processCalculation()

mask(layer1,VIS_RAD)

def mask (ivp,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='ivp@1'
   raster1.raster=ivp
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("ivp@1"*%s)+(%s)'%(ganho_ivp,offset_ivp) ,output,'GTiff',ivp.extent(),ivp.width(),ivp.height(),entries)
   calc.processCalculation()

mask(layer2,IVP_RAD)

layer3 = processing.getObject(VIS_RAD)
layer4 = processing.getObject(IVP_RAD)

def mask (VIS_RAD,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='VIS_RAD@1'
   raster1.raster=VIS_RAD
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("VIS_RAD@1"*%s)'%coef_vis ,output,'GTiff',VIS_RAD.extent(),VIS_RAD.width(),VIS_RAD.height(),entries)
   calc.processCalculation()

mask(layer3,VIS_REFLEC)

def mask (IVP_RAD,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IVP_RAD@1'
   raster1.raster=IVP_RAD
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("IVP_RAD@1"*%s)'%coef_ivp ,output,'GTiff',IVP_RAD.extent(),IVP_RAD.width(),IVP_RAD.height(),entries)
   calc.processCalculation()

mask(layer4,IVP_REFLEC)

layer5 = processing.getObject(VIS_REFLEC)
layer6 = processing.getObject(IVP_REFLEC)

def mask (VIS_REFLEC,IVP_REFLEC, output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IVP_REFLEC@1'
   raster1.raster=IVP_REFLEC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='VIS_REFLEC@1'
   raster2.raster=VIS_REFLEC
   raster2.bandNumber=1
   entries.append(raster2)
   
   calc=QgsRasterCalculator('("IVP_REFLEC@1"-"VIS_REFLEC@1")/("IVP_REFLEC@1"+"VIS_REFLEC@1")',output,'GTiff',VIS_REFLEC.extent(),VIS_REFLEC.width(),VIS_REFLEC.height(),entries)
   calc.processCalculation()

mask(layer5,layer6,NDVI)

layer7 = processing.getObject(NDVI)

def mask (NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='NDVI@1'
   raster1.raster=NDVI
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('(0.75 + (2E-5*("NDVI@1"/"NDVI@1")*%s))'%altitude,output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()

mask(layer7,TRANSMITIVIDADE_ATM)

layer8 = processing.getObject(TRANSMITIVIDADE_ATM)

def mask (TRANSMITIVIDADE_ATM,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='TRANSMITIVIDADE_ATM@1'
   raster1.raster=TRANSMITIVIDADE_ATM
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(0.85*((-1*(ln("TRANSMITIVIDADE_ATM@1")))^0.09))' ,output,'GTiff',TRANSMITIVIDADE_ATM.extent(),TRANSMITIVIDADE_ATM.width(),TRANSMITIVIDADE_ATM.height(),entries) 
   calc.processCalculation()

mask(layer8,EMISSIVIDADE_ATM)

layer9 = processing.getObject(EMISSIVIDADE_ATM)

def mask (EMISSIVIDADE_ATM,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='EMISSIVIDADE_ATM@1'
   raster1.raster=EMISSIVIDADE_ATM
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("EMISSIVIDADE_ATM@1"*(5.67e-8)*(%s^4))'%temp,output,'GTiff',EMISSIVIDADE_ATM.extent(),EMISSIVIDADE_ATM.width(),EMISSIVIDADE_ATM.height(),entries) 
   calc.processCalculation()

mask(layer9,LIN)

def mask (NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='NDVI@1'
   raster1.raster=NDVI
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("NDVI@1">=0.24)*((1.0094)+(0.10824*log10("NDVI@1")))',output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()

mask(layer7,EMISSIVIDADE_VEG)

def mask (NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='NDVI@1'
   raster1.raster=NDVI
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('("NDVI@1"<0.24)*0.94',output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()

mask(layer7,EMISSIVIDADE_SOLO)

layer10 = processing.getObject(EMISSIVIDADE_VEG)
layer11 = processing.getObject(EMISSIVIDADE_SOLO)

def mask (NDVI, output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='NDVI@1'
   raster1.raster=NDVI
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(("NDVI@1">=0.24)*1)*%s' %temp ,output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()

mask(layer7,TEMP_VEG)

def mask (NDVI, output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='NDVI@1'
   raster1.raster=NDVI
   raster1.bandNumber=1
   entries.append(raster1)
    
   calc=QgsRasterCalculator('(("NDVI@1<0.24)*1)*%s' %temp,output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()

mask(layer7,TEMP_SOLO)

layer25 = processing.getObject(TEMP_VEG)
layer26 = processing.getObject(TEMP_SOLO)

#Estatisticas dos rasters

provider1 = layer25.dataProvider()
ext1 = layer25.extent()
stats1 = provider1.bandStatistics(1,QgsRasterBandStats.All,ext1,0)

provider2 = layer26.dataProvider()
ext2 = layer26.extent()
stats2 = provider2.bandStatistics(1,QgsRasterBandStats.All,ext1,0)

media_veg = stats1.mean
media_solo = stats2.mean 

fr=(stats1.sum/stats1.maximumValue)/stats1.elementCount

def mask (EMISSIVIDADE_VEG,NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='EMISSIVIDADE_VEG@1'
   raster1.raster=EMISSIVIDADE_VEG
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='NDVI@1'
   raster2.raster=NDVI
   raster2.bandNumber=1
   entries.append(raster2)
   
   calc=QgsRasterCalculator('((("NDVI@1">=0.24)*(%s^4))*"EMISSIVIDADE_VEG@1"*5.67e-8)'%media_veg,output,'GTiff',EMISSIVIDADE_VEG.extent(),EMISSIVIDADE_VEG.width(),EMISSIVIDADE_VEG.height(),entries)
   calc.processCalculation()

mask(layer10,layer7,LOUTC)

def mask (EMISSIVIDADE_SOLO,NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='EMISSIVIDADE_SOLO@1'
   raster1.raster=EMISSIVIDADE_SOLO
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='NDVI@1'
   raster2.raster=NDVI
   raster2.bandNumber=1
   entries.append(raster2)   
   
   calc=QgsRasterCalculator('((("NDVI@1"<0.24)*(%s^4))*"EMISSIVIDADE_SOLO@1"*5.67e-8)'%media_solo,output,'GTiff',EMISSIVIDADE_SOLO.extent(),EMISSIVIDADE_SOLO.width(),EMISSIVIDADE_SOLO.height(),entries)
   calc.processCalculation()

mask(layer11,layer7,LOUTS)

def mask (TRANSMITIVIDADE_ATM,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='TRANSMITIVIDADE_ATM@1'
   raster1.raster=TRANSMITIVIDADE_ATM
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(%s*(%s)*(cos(%s))*("TRANSMITIVIDADE_ATM@1"))'%(esun_sol,dist_terra_sol,elev_rad) ,output,'GTiff',TRANSMITIVIDADE_ATM.extent(),TRANSMITIVIDADE_ATM.width(),TRANSMITIVIDADE_ATM.height(),entries) 
   calc.processCalculation()

mask(layer8,RSE)


def mask (VIS_REFLEC,IVP_REFLEC,NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IVP_REFLEC@1'
   raster1.raster=IVP_REFLEC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='NDVI@1'
   raster2.raster=NDVI
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='VIS_REFLEC@1'
   raster3.raster=VIS_REFLEC
   raster3.bandNumber=1
   entries.append(raster3)
      
   calc=QgsRasterCalculator('("NDVI@1">=0.24)*(("IVP_REFLEC@1"*%s)+("IVP_REFLEC@1"*%s))'%(coef_albedo_ivp,coef_albedo_vis),output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries) 
   calc.processCalculation()

mask(layer5,layer6,layer7,ALBEDO_VEG)

def mask (VIS_REFLEC,IVP_REFLEC,NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IVP_REFLEC@1'
   raster1.raster=IVP_REFLEC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='NDVI@1'
   raster2.raster=NDVI
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='VIS_REFLEC@1'
   raster3.raster=VIS_REFLEC
   raster3.bandNumber=1
   entries.append(raster3)
      
   calc=QgsRasterCalculator('("NDVI@1"<0.24)*(("IVP_REFLEC@1"*%s)+("IVP_REFLEC@1"*%s))'%(coef_albedo_ivp,coef_albedo_vis),output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries) 
   calc.processCalculation()

mask(layer5,layer6,layer7,ALBEDO_SOLO)

layer12 = processing.getObject(ALBEDO_VEG)
layer13 = processing.getObject(RSE)
layer14 = processing.getObject(LIN)
layer15 = processing.getObject(LOUTC)
layer16 = processing.getObject(LOUTS)
layer17 = processing.getObject(ALBEDO_SOLO)


def mask (ALBEDO_VEG,RSE,LIN,LOUTC,EMISSIVIDADE_VEG,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='ALBEDO_VEG@1'
   raster1.raster=ALBEDO_VEG
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='RSE@1'
   raster2.raster=RSE
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='LIN@1'
   raster3.raster=LIN
   raster3.bandNumber=1
   entries.append(raster3)
   
   raster4=QgsRasterCalculatorEntry()
   raster4.ref='LOUTC@1'
   raster4.raster=LOUTC
   raster4.bandNumber=1
   entries.append(raster4)
   
   raster5=QgsRasterCalculatorEntry()
   raster5.ref='EMISSIVIDADE_VEG@1'
   raster5.raster=EMISSIVIDADE_VEG
   raster5.bandNumber=1
   entries.append(raster5)
      
   calc=QgsRasterCalculator('((1-"ALBEDO_VEG@1")*"RSE@1")+"LIN@1"-"LOUTC@1"-((1-"EMISSIVIDADE_VEG@1")*"LIN@1")',output,'GTiff',RSE.extent(),RSE.width(),RSE.height(),entries) 
   calc.processCalculation()

mask(layer12,layer13,layer14,layer15,layer10,RNC)

def mask (ALBEDO_SOLO,RSE,LIN,LOUTS,EMISSIVIDADE_SOLO,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='ALBEDO_SOLO@1'
   raster1.raster=ALBEDO_SOLO
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='RSE@1'
   raster2.raster=RSE
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='LIN@1'
   raster3.raster=LIN
   raster3.bandNumber=1
   entries.append(raster3)
   
   raster4=QgsRasterCalculatorEntry()
   raster4.ref='LOUTS@1'
   raster4.raster=LOUTS
   raster4.bandNumber=1
   entries.append(raster4)
   
   raster5=QgsRasterCalculatorEntry()
   raster5.ref='EMISSIVIDADE_SOLO@1'
   raster5.raster=EMISSIVIDADE_SOLO
   raster5.bandNumber=1
   entries.append(raster5)
    
   calc=QgsRasterCalculator('((1-"ALBEDO_SOLO@1")*"RSE@1")+"LIN@1"-"LOUTS@1"-((1-"EMISSIVIDADE_SOLO@1")*"LIN@1")',output,'GTiff',RSE.extent(),RSE.width(),RSE.height(),entries) 
   calc.processCalculation()

mask(layer17,layer13,layer14,layer16,layer11,RNS)

layer18 = processing.getObject(RNC)
layer19 = processing.getObject(RNS)

def mask (RNC,RNS,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='RNC@1'
   raster1.raster=RNC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='RNS@1'
   raster2.raster=RNS
   raster2.bandNumber=1
   entries.append(raster2)
         
   calc=QgsRasterCalculator('%s*"RNC@1"+(1-%s)*"RNS@1"'%(fr,fr),output,'GTiff',RNC.extent(),RNC.width(),RNC.height(),entries) 
   calc.processCalculation()

mask(layer18,layer19,RNE)

def mask (IVP_REFLEC,VIS_REFLEC,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IVP_REFLEC@1'
   raster1.raster=IVP_REFLEC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='VIS_REFLEC@1'
   raster2.raster=VIS_REFLEC
   raster2.bandNumber=1
   entries.append(raster2)
      
   calc=QgsRasterCalculator('(1.5*("IVP_REFLEC@1"-"VIS_REFLEC@1"))/(0.5+("IVP_REFLEC@1"+"VIS_REFLEC@1"))',output,'GTiff',IVP_REFLEC.extent(),IVP_REFLEC.width(),IVP_REFLEC.height(),entries)
   calc.processCalculation()

mask(layer6,layer5,SAVI)

layer20 = processing.getObject(SAVI)

def mask (SAVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='SAVI@1'
   raster1.raster=SAVI
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(-1*((ln((0.69-"SAVI@1")/0.59))/0.91))',output,'GTiff',SAVI.extent(),SAVI.width(),SAVI.height(),entries)
   calc.processCalculation()

mask(layer20,IAF)

layer21 = processing.getObject(IAF)

def mask (IAF,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IAF@1'
   raster1.raster=IAF
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('("IAF@1">=0.5)*(25/"IAF@1")',output,'GTiff',IAF.extent(),IAF.width(),IAF.height(),entries)
   calc.processCalculation()

mask(layer21,RAC)

RAS0 = (log(alt_referencia/(0.05*alt_dossel*0.1)))*(log((0.63*alt_dossel+(0.05*alt_dossel*0.1))/(0.05*alt_dossel*0.1)))/((vento*0.41)**2)
RAS1 = (((log((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel*0.1)))/(vento*0.41)**2)*(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(exp(2.5)-exp(2.5*(1-((0.63*alt_dossel)+((0.05*alt_dossel*0.1)/alt_dossel)))))
RAA0 = (((log(alt_referencia/(0.05*alt_dossel*0.1)))**2)/((vento*0.41)**2))-RAS0
RAA1 = ((log((alt_referencia-(0.63*alt_dossel))/(0.05*alt_dossel)))/((vento*0.41)**2))*((log((alt_referencia-(0.63*alt_dossel))/(alt_dossel-(0.63*alt_dossel))))+(alt_dossel/(2.5*(alt_dossel-(0.63*alt_dossel)))))*(exp(2.5*(1-(((alt_dossel*0.63)+(0.05*alt_dossel))/alt_dossel)))-1)

def mask (IAF, output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IAF@1'
   raster1.raster=IAF
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(("IAF@1"/10)*%s)+(((4-"IAF@1")/10)*%s)'%(RAS1,RAS0) ,output,'GTiff',IAF.extent(),IAF.width(),IAF.height(),entries)
   calc.processCalculation()

mask(layer21,RAS)

layer22 = processing.getObject(RAS)

def mask (IAF,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='IAF@1'
   raster1.raster=IAF
   raster1.bandNumber=1
   entries.append(raster1)
   
   calc=QgsRasterCalculator('(("IAF@1"/20)*%s)+(((4-"IAF@1")/20)*%s)'%(RAA1,RAA0) ,output,'GTiff',IAF.extent(),IAF.width(),IAF.height(),entries)
   calc.processCalculation()

mask(layer21,RAA)

layer23 = processing.getObject(RAA)
layer24 = processing.getObject(RAC)


def mask (RAA,RAC,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='RAA@1'
   raster1.raster=RAA
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='RAC@1'
   raster2.raster=RAC
   raster2.bandNumber=1
   entries.append(raster2)
    
   calc=QgsRasterCalculator('(1.15*1005*0.10)/("RAC@1"+"RAA@1")',output,'GTiff',RAC.extent(),RAC.width(),RAC.height(),entries)
   calc.processCalculation()

mask(layer23,layer24,HC)

def mask (RAA,RAS,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='RAA@1'
   raster1.raster=RAA
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='RAS@1'
   raster2.raster=RAS
   raster2.bandNumber=1
   entries.append(raster2)
            
   calc=QgsRasterCalculator('(1.15*1005*0.13)/("RAS@1"+"RAA@1")',output,'GTiff',RAS.extent(),RAS.width(),RAS.height(),entries)
   calc.processCalculation()

mask(layer23,layer22,HS)

layer27 = processing.getObject(HC)
layer28 = processing.getObject(HS)

def mask (HC,HS,NDVI,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='HC@1'
   raster1.raster=HC
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='HS@1'
   raster2.raster=HS
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='NDVI@1'
   raster3.raster=NDVI
   raster3.bandNumber=1
   entries.append(raster3)
      
   calc=QgsRasterCalculator('%s*"HC@1"+(1-%s)*"HS@1"'%(fr,fr),output,'GTiff',NDVI.extent(),NDVI.width(),NDVI.height(),entries)
   calc.processCalculation()
mask(layer27,layer28,layer7,HE)

layer29 = processing.getObject(RNE)

def mask (RNE,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='RNE@1'
   raster1.raster=RNE
   raster1.bandNumber=1
   entries.append(raster1)
      
   calc=QgsRasterCalculator('(0.3236*("RNE@1")-51.52)' ,output,'GTiff',RNE.extent(),RNE.width(),RNE.height(),entries)
   calc.processCalculation()

mask(layer29,GE)

layer30 = processing.getObject(GE)
layer31 = processing.getObject(HE)


def mask (RNE,HE,GE,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='RNE@1'
   raster1.raster=RNE
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='HE@1'
   raster2.raster=HE
   raster2.bandNumber=1
   entries.append(raster2)
   
   raster3=QgsRasterCalculatorEntry()
   raster3.ref='GE@1'
   raster3.raster=GE
   raster3.bandNumber=1
   entries.append(raster3)
      
   calc=QgsRasterCalculator('"RNE@1"-"HE@1"-"GE@1"',output,'GTiff',GE.extent(),GE.width(),GE.height(),entries)
   calc.processCalculation()

mask(layer29,layer30,layer31,LEE)

def mask (EMISSIVIDADE_VEG,EMISSIVIDADE_SOLO,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='EMISSIVIDADE_VEG@1'
   raster1.raster=EMISSIVIDADE_VEG
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='EMISSIVIDADE_SOLO@1'
   raster2.raster=EMISSIVIDADE_SOLO
   raster2.bandNumber=1
   entries.append(raster2)
        
   calc=QgsRasterCalculator('((2.501-0.00236*((%s*("EMISSIVIDADE_VEG@1"+"EMISSIVIDADE_SOLO@1"))-273.16))*(1e6))' %temp,output,'GTiff',EMISSIVIDADE_VEG.extent(),EMISSIVIDADE_VEG.width(),EMISSIVIDADE_VEG.height(),entries)
   calc.processCalculation()

mask(layer10,layer11,LAMBDA)

layer32 = processing.getObject(LEE)
layer33 = processing.getObject(LAMBDA)

def mask (LEE,LAMBDA,output):
   entries=[]

   raster1=QgsRasterCalculatorEntry()
   raster1.ref='LEE@1'
   raster1.raster=LEE
   raster1.bandNumber=1
   entries.append(raster1)
   
   raster2=QgsRasterCalculatorEntry()
   raster2.ref='LAMBDA@1'
   raster2.raster=LAMBDA
   raster2.bandNumber=1
   entries.append(raster2)
      
   calc=QgsRasterCalculator('(3600*"LEE@1")/"LAMBDA@1"',output,'GTiff',LEE.extent(),LEE.width(),LEE.height(),entries)
   calc.processCalculation()

mask(layer29,layer33,ET)
