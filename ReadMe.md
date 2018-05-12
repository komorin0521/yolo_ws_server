# Overview
This is a websocket server using [darknet yolo](https://pjreddie.com/darknet/yolo/)

# Environment
- Python: 2.7(.12)
    I checked the 2.7.12 only

- darknet
    revision is `259be3217b0331d07c8c5c1995d90ab9f3b768c1`


# SetUp
## 1. Installing darknet 
See [yolo](https://pjreddie.com/darknet/yolo/)
After cloning darknet please checkout revision ``

```bash
$ cd ${HOME}/darknet_ws/darknet
$ git checkout 259be3217b0331d07c8c5c1995d90ab9f3b768c1
```

Then please make.


## 2. install libs using pip
```bash
$ pip install -r requirements.txt
```

## 3. Setting scripts under the `path_to_darknet/python`
This explanation is cloning darknet under the `${HOME}/darknet_ws`

```bash
$ cp *.py ${HOME}/darknet_ws/darknet/python/
$ cp -r config  ~/darknet_ws/darkent/python/
$ cd ${HOME}/darknet_ws/darknet/python
$ ln -s ../data data
```

## 4. Modify config
Please modify `config/yolo_ws_server.ini`

## 5. Run scripts
```bash
$ cd ${HOME}/darkent_ws/darknet/python
$ python ./darknet_ws_server.py
```
# Contacts
If you have any questions, please send me an email or pull request.

email: yu.omori0521@gmail.com
