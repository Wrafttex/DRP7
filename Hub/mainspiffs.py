import os
import spiffsgen as sg

# Based on typedefs under spiffs_config.h
SPIFFS_OBJ_ID_LEN = 2  # spiffs_obj_id
SPIFFS_SPAN_IX_LEN = 2  # spiffs_span_ix
SPIFFS_PAGE_IX_LEN = 2  # spiffs_page_ix
SPIFFS_BLOCK_IX_LEN = 2  # spiffs_block_ix

BASE_DIR = "data"

def make_spiffs(output_file="./Hub/static/ESP_DATA/spiffs.bin",
                image_size="0xf000",
                page_size=256,
                block_size=4096,
                obj_name_len=32,
                meta_len=4,
                use_magic=True,
                follow_symlinks=False,
                use_magic_len=True,
                big_endian=False):
    
    if not os.path.exists(BASE_DIR):
        raise RuntimeError('given base directory %s does not exist' % BASE_DIR)

    with open(output_file, 'wb') as image_file:
        image_size = int(image_size, 0)
        spiffs_build_default = sg.SpiffsBuildConfig(page_size, SPIFFS_PAGE_IX_LEN,
                                                 block_size, SPIFFS_BLOCK_IX_LEN, meta_len,
                                                 obj_name_len, SPIFFS_OBJ_ID_LEN, SPIFFS_SPAN_IX_LEN,
                                                 True, True, 'big' if big_endian else 'little',
                                                 use_magic, use_magic_len)

        spiffs = sg.SpiffsFS(image_size, spiffs_build_default)

        for root, dirs, files in os.walk(BASE_DIR, followlinks=follow_symlinks):
            for f in files:
                full_path = os.path.join(root, f)
                spiffs.create_file('/' + os.path.relpath(full_path, BASE_DIR).replace('\\', '/'), full_path)

        image = spiffs.to_binary()

        image_file.write(image)

def mainspiffs(room_name:str, ssid:str, wifi_pass: str, mqtt_host: str, mqtt_port: int, mqtt_user: str, mqtt_pass: str):

    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    with open(BASE_DIR + "/room_name", 'w') as room_name:
        room_name.write(ssid)

    with open(BASE_DIR + "/wifi-ssid", 'w') as wifiSsid:
        wifiSsid.write(ssid)

    with open(BASE_DIR + "/wifi-password", 'w') as wifiPass:
        wifiPass.write(wifi_pass)

    with open(BASE_DIR + "/mqtt_host", 'w') as mqttHost:
        mqttHost.write(mqtt_host)

    with open(BASE_DIR + "/mqtt_port", 'w') as mqttPort:
        mqttPort.write(mqtt_port)

    with open(BASE_DIR + "/mqtt_user", 'w') as mqttUser:
        mqttUser.write(mqtt_user)

    with open(BASE_DIR + "/mqtt_pass", 'w') as mqttPass:
        mqttPass.write(mqtt_pass)

    make_spiffs()

if __name__ == '__main__':
    mainspiffs("","","","","","")