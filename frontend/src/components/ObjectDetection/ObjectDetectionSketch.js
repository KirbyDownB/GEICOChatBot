import * as p5 from 'p5'
import "p5/lib/addons/p5.dom";
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import * as faceapi from 'face-api.js';
//import worker from "../../worker.js";
//import WebWorker from "../../workerSetup";

const MODEL_URL = '/models'

export default function sketch (p) {
    // let global = [];
    //let w = new WebWorker(worker);

    let capture = null;
    // let cocossdModel = null;
    //
    // let cocoDrawings = [];
    // let faceDrawings = [];
    //
    // function showCocoSSDResults(results) {
    //     cocoDrawings = results;
    // }
    //
    // function showFaceDetectionData(data) {
    //     faceDrawings = data;
    // }

    p.setup = async function () {

        await Promise.all([
          faceapi.loadTinyFaceDetectorModel(MODEL_URL),
          // faceapi.loadSsdMobilenetv1Model(MODEL_URL),
          faceapi.loadFaceExpressionModel(MODEL_URL)
        ])



        p.createCanvas(1, 1);
        const constraints = {
            video: {
              optional: [{ maxFrameRate: 5 }]
            },
            audio: false
          };

        capture = p.createCapture(constraints, () => {
        });


        capture.id("video_element");
        //capture.size(200, 200);
        capture.hide();

        // cocoSsd.load().then((model) => {
        //     try {
        //         cocossdModel = model;
        //     } catch(e) {
        //         console.log(e);
        //     }
        //
        // }).catch((e) => {
        //     console.log("Error occured : ", e);
        // });

    };

    p.draw = async () => {
        if (!capture) {
            return;
        }
        //p.image(capture, 0, 0);
        //p.fill(247, 248, 255, 1);

        // cocoDrawings.map((drawing) => {
        //     if (drawing) {
        //         p.textSize(20);
        //         p.strokeWeight(1);
        //         const textX = drawing.bbox[0]+drawing.bbox[2];
        //         const textY = drawing.bbox[1]+drawing.bbox[3];
        //
        //         const confidenetext = "Confidence: "+ drawing.score.toFixed(1);
        //         const textWidth = p.textWidth(confidenetext);
        //
        //         const itemTextWidth = p.textWidth(drawing.class);
        //         p.text(drawing.class, textX-itemTextWidth-10, textY-50);
        //
        //         p.text(confidenetext, textX-textWidth-10, textY-10);
        //         p.strokeWeight(4);
        //         p.stroke('rgb(100%,100%,100%)');
        //         p.rect(drawing.bbox[0], drawing.bbox[1], drawing.bbox[2], drawing.bbox[3]);
        //     }
        // });

        // faceDrawings.map((drawing) => {
        //     if (drawing) {
        //         p.textSize(15);
        //         p.strokeWeight(1);
        //
        //         const textX = drawing.detection.box._x+drawing.detection.box._width;
        //         const textY = drawing.detection.box._y+drawing.detection.box._height;
        //
        //         const copiedExpression = drawing.expressions;
        //         const expressions = Object.keys(copiedExpression).map((key) => {
        //             const value = copiedExpression[key];
        //             return value;
        //         })
        //
        //         const max = Math.max(...expressions);
        //
        //         const expression_value = Object.keys(copiedExpression).filter((key) => {
        //             return copiedExpression[key] === max;
        //         })[0];
        //
        //         const expressiontext = "Mood: "+ expression_value;
        //         const expressionWidth = p.textWidth(expressiontext);
        //         p.text(expressiontext, textX-expressionWidth-10, textY-10);
        //
        //         p.strokeWeight(4);
        //         p.stroke('rgb(100%,100%,100%)');
        //         p.rect(drawing.detection.box._x, drawing.detection.box._y, drawing.detection.box._width, drawing.detection.box._height);
        //     }
        // });



        p.myCustomRedrawAccordingToNewPropsHandler = function(newProps){
          // console.log(global)
          // console.log(newProps.hello)
          newProps.handleExpression(global)
          faceapi.detectAllFaces(capture.id(), new faceapi.TinyFaceDetectorOptions()).withFaceExpressions().then((data) => {
            if (data[0] && data[0].expressions){
              //console.log(data[0].expressions)
              newProps.handleExpression(data[0].expressions)
              console.log(faceapi.tf.getBackend())
            }

              //howFaceDetectionData(data);
          });
        }


    }
  };
