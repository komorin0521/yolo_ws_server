#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Yolo Web Socekt Server using yolo python IF.
Author: yu.oomori
Email: yu.oomori0521@gmail.com
"""


import base64
import ConfigParser
import logging
import os
import StringIO
import sys

import cv2
import numpy as np
from PIL import Image
from websocket_server import WebsocketServer

from darknet import Yolo


class YoloWsServer(object):
    """
    Yolo Web Socket Server class
    """

    def __init__(self, host, port, cfgfilepath, weightfilepath, datafilepath):
        """
        Initialization
        """

        # Web socket server init
        self._host = host
        self._port = port
        self._ws_server = WebsocketServer(host=host,
                                          port=port,
                                          loglevel=logging.INFO)
        self._ws_server.set_fn_new_client(self._new_client)
        self._ws_server.set_fn_client_left(self._client_left)
        self._ws_server.set_fn_message_received(self._message_received)

        # Yolo Model Init
        self._yolo = Yolo(cfgfilepath, datafilepath, weightfilepath)

        # setting logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            ' %(module)s -  %(asctime)s - %(levelname)s - %(message)s'))
        self._logger.addHandler(handler)

    def _new_client(self, client, server):
        """
        callback function when new client connected
        """

        self._logger.info('New client %s:%s has joined.' %
                          (str(client['address'][0]), str(client['address'][1])))

    def _client_left(self, client, server):
        """
        callback function when a client disconnect
        """

        self._logger.info('Client %s:%s has left.' %
                          (str(client['address'][0]), str(client['address'][1])))

    def _message_received(self, client, server, message):
        """
        callback function when a client send message
        """

        self._logger.info('Message has been received from %s:%s' %
                          (str(client['address'][0]), str(client['address'][1])))
        try:
            img_data = base64.b64decode(message)
            img = np.array(Image.open(
                StringIO.StringIO(img_data)).convert("RGB"))
            yolo_results = self._yolo.predict(img)
            img = self._yolo.draw_detections(img, yolo_results)
            _, buf = cv2.imencode(".png", img)
            pred_img_data = base64.b64encode(buf)
            server.send_message(client, pred_img_data)
        except Exception as err:
            self._logger.info("failed")
            self._logger.error(err)

    def run_forever(self):
        """
        Running ws server
        """

        self._logger.info("runnning on ws://%s:%d" % (self._host, self._port))
        self._ws_server.run_forever()


def get_params(configfilepath):
    """
    Getting configfile from configfilepath
    configfilepath: str
    """

    config_parser = ConfigParser.ConfigParser()
    if not os.path.exists(configfilepath):
        raise NameError("%s does not exit" % configfilepath)

    config_parser.read(configfilepath)

    try:
        host = config_parser.get("SERVER", "host")
        port = config_parser.getint("SERVER", "port")

        cfgfilepath = config_parser.get("YOLO", "cfgfilepath")
        datafilepath = config_parser.get("YOLO", "datafilepath")
        weightfilepath = config_parser.get("YOLO", "weightfilepath")
        return host, port, cfgfilepath, datafilepath, weightfilepath

    except ConfigParser.Error as config_err:
        print config_err
        print type(config_err)
        raise config_err


def main():
    """
    main function
    """
    configfilepath = "./config/yolo_ws_server.ini"

    try:
        host, port, cfgfilepath, datafilepath, weightfilepath = get_params(
            configfilepath)

        ws_server = YoloWsServer(host=host,
                                 port=port,
                                 cfgfilepath=cfgfilepath,
                                 weightfilepath=weightfilepath,
                                 datafilepath=datafilepath)
        ws_server.run_forever()
    except (ConfigParser.Error, NameError) as err:
        print err
        sys.exit(1)


if __name__ == "__main__":
    main()
