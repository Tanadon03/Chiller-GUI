import paho.mqtt.publish as publish
import read_elec as elec
import read_sensor as water


def sent_data_to_nodered():
    #electric variable
    V=str(elec.get_voltage())
    C=str(elec.get_current())
    P=str(elec.get_power())
    E=str(elec.get_energy())
    PF=str(elec.get_powerfactor())
    F=str(elec.get_frequency())
    
    #water variable
    Temp=str(water.get_temperature())
    pH=str(water.get_pH())
    calibration=str(water.get_calibration())
    EC=str(water.get_EC())
    TDS=str(water.get_TDS())
    
    data_elec="\"Voltage\":\"{v}\",\"Current\":\"{c}\",\"Power\":\"{p}\",\"Energy\":\"{e}\",\"Powerfactor\":\"{pf}\",\"Frequency\":\"{f}\"".format(v=V,c=C,p=P,e=E,pf=PF,f=F)
    data_water="\"Temperature\":\"{t}\",\"pH\":\"{ph}\",\"Calibration\":\"{c}\",\"EC\":\"{ec}\",\"TDS\":\"{tds}\"".format(t=Temp,ph=pH,c=calibration,ec=EC,tds=TDS)
    
    
    publish.single("chiller/data/elec",data_elec,hostname="192.168.137.1")
    publish.single("chiller/data/water_quality",data_water,hostname="192.168.137.1")
    print("All data have already sent")