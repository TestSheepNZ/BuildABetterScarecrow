import argparse
import base64
import json
import sys
import requests
from SoundControl import SoundControl
from WebCamCapture import WebCamCapture
import time

DETECTION_TYPES = [
    'TYPE_UNSPECIFIED',
    'FACE_DETECTION',
    'LANDMARK_DETECTION',
    'LOGO_DETECTION',
    'LABEL_DETECTION',
    'TEXT_DETECTION',
    'SAFE_SEARCH_DETECTION',
]


def get_detection_type(detect_num):
    """Return the Vision API symbol corresponding to the given number."""
    detect_num = int(detect_num)
    if 0 < detect_num < len(DETECTION_TYPES):
        return DETECTION_TYPES[detect_num]
    else:
        return DETECTION_TYPES[0]


class Label:
    description = ""
    score=0

class ItemOfInterest:
    tag = ""
    tagList = list()
    threshold = 0
    priority = 0
    coolDown = 0
    lastTriggered = 0
    nextTrigger = 0
    audioResponse = ""
    visualResponse = ""

    def setTriggered(self):
        self.lastTriggered = int(time.time())
        self.nextTrigger = self.lastTriggered + self.coolDown

    def matchesLabel(self, labelName, labelScore, currentPriority):
        currentTime = time.time()
        if currentTime > self.coolDown:
            for thisTag in self.tagList:
                if thisTag in labelName:
                    if labelScore > self.threshold:
                        if self.priority < currentPriority:
                            return True
        return False

    def getPriority(self):
        return self.priority

    def triggerResponse(self):
        self.setTriggered()
        soundDisplay = SoundControl()
        soundDisplay.soundAndImageDisplay(self.audioResponse, self.visualResponse, "API Matched Item")


class GoogleVisionRequest:
    response = ""
    output_filename = "capture/json_image.json"
    projectAPIKey = "YOU NEED YOUR OWN HERE"
    labelList = list()
    itemList = list()

    def initialiseResponses(self):
        self.itemList.clear()
        baseThreshold = 0.4

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("crow")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 1
        itemToCheck.audioResponse = "sounds/crow.wav"
        itemToCheck.visualResponse = "images/crow.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("bird")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 5
        itemToCheck.audioResponse = "sounds/bird.wav"
        itemToCheck.visualResponse = "images/bird.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("banana")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 10
        itemToCheck.audioResponse = "sounds/banana.wav"
        itemToCheck.visualResponse = "images/banana.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("apple")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 20
        itemToCheck.audioResponse = "sounds/apple.wav"
        itemToCheck.visualResponse = "images/apple.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("tangerine")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 22
        itemToCheck.audioResponse = "sounds/tangerine.wav"
        itemToCheck.visualResponse = "images/orange.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("mandarin")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 22
        itemToCheck.audioResponse = "sounds/mandarin.wav"
        itemToCheck.visualResponse = "images/orange.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("orange")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 24
        itemToCheck.audioResponse = "sounds/orange.wav"
        itemToCheck.visualResponse = "images/orange.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("kiwi")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 25
        itemToCheck.audioResponse = "sounds/kiwi.wav"
        itemToCheck.visualResponse = "images/kiwi.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("mango")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 22
        itemToCheck.audioResponse = "sounds/mango.wav"
        itemToCheck.visualResponse = "images/mango.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("fruit")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 50
        itemToCheck.audioResponse = "sounds/fruit.wav"
        itemToCheck.visualResponse = "images/fruit.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("food")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 60
        itemToCheck.audioResponse = "sounds/food.wav"
        itemToCheck.visualResponse = "images/food.jpg"
        self.itemList.append(itemToCheck)


        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("produce")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 60
        itemToCheck.audioResponse = "sounds/vegetable.wav"
        itemToCheck.visualResponse = "images/fruit.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("cup")
        itemToCheck.tagList.append("drink")
        itemToCheck.tagList.append("coffee")
        itemToCheck.tagList.append("tea")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 65
        itemToCheck.audioResponse = "sounds/cup.wav"
        itemToCheck.visualResponse = "images/cup.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("pen")
        itemToCheck.tagList.append("pencil")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 80
        itemToCheck.audioResponse = "sounds/pen.wav"
        itemToCheck.visualResponse = "images/pen.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("utensil")
        itemToCheck.tagList.append("cutlery")
        itemToCheck.tagList.append("knife")
        itemToCheck.tagList.append("fork")
        itemToCheck.tagList.append("spoon")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 75
        itemToCheck.audioResponse = "sounds/forks.wav"
        itemToCheck.visualResponse = "images/forks.jpg"
        self.itemList.append(itemToCheck)

        itemToCheck = ItemOfInterest()
        itemToCheck.tagList = list()
        itemToCheck.tagList.append("human")
        itemToCheck.tagList.append("man")
        itemToCheck.tagList.append("woman")
        itemToCheck.tagList.append("boy")
        itemToCheck.tagList.append("girl")
        itemToCheck.tagList.append("people")
        itemToCheck.tagList.append("person")
        itemToCheck.threshold = baseThreshold
        itemToCheck.priority = 95
        itemToCheck.audioResponse = "sounds/human.wav"
        itemToCheck.visualResponse = "images/human.jpg"
        self.itemList.append(itemToCheck)

    def takePicture(self):
        self.initialiseResponses()
        snapShot = WebCamCapture()
        features = "4:20"
        if (snapShot.pictureCountdown()):
            self.preparePicture(snapShot.getPictureName(), features)
            self.sendPictureToAPI()

            pictureMatch = False
            currentMatch = ItemOfInterest()
            currentMatch.priority = 100

            for visualLabel in self.labelList:
                for itemOfInterest in self.itemList:
                    if itemOfInterest.matchesLabel(visualLabel.description, visualLabel.score, currentMatch.priority ):
                        currentMatch = itemOfInterest
                        pictureMatch = True
            if pictureMatch:
                currentMatch.triggerResponse()
            else:
                print ("No match")
                #snapShot.deletePicture()


    def preparePicture(self, imageFilename, features):

        request_list = []
        with open(imageFilename, 'rb') as image_file:
            content_json_obj = {
                'content': base64.b64encode(image_file.read()).decode('UTF-8')
            }

        feature_json_obj = []
        for word in features.split(' '):
            feature, max_results = word.split(':', 1)
            feature_json_obj.append({
                'type': get_detection_type(feature),
                'maxResults': int(max_results),
            })

        request_list.append({
            'features': feature_json_obj,
            'image': content_json_obj,
        })

        with open(self.output_filename, 'w') as output_file:
            json.dump({'requests': request_list}, output_file)

    def sendPictureToAPI(self):
        data = open(self.output_filename)
        self.labelList.clear()

        urlRequest = "https://vision.googleapis.com/v1/images:annotate?key=" + self.projectAPIKey
        print(urlRequest)
        response = requests.post(url=urlRequest,
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
        dataList = response.json()

        for responseItem in dataList['responses']:
            for labelItem in responseItem['labelAnnotations']:
                labelDetails = Label()
                labelDetails.description = labelItem['description']
                labelDetails.score = labelItem['score']
                self.labelList.append(labelDetails)

        print("API Response")
        for thisThing in self.labelList:
            print (thisThing.description + " = " + str(thisThing.score))

visionRequest = GoogleVisionRequest()
#for x in range(1, 10):
#    visionRequest = GoogleVisionRequest()
visionRequest.takePicture()
