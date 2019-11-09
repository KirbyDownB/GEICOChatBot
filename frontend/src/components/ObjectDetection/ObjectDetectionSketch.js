import * as p5 from 'p5'
import "p5/lib/addons/p5.dom";
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import * as faceapi from 'face-api.js';

const MODEL_URL = '/models'

export default function sketch (p) {
    let capture = null;

    p.setup = async function () {
        await Promise.all([
          faceapi.loadTinyFaceDetectorModel(MODEL_URL),
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
        capture.hide();
    };

    p.draw = async () => {
        if (!capture) {
            return;
        }
        p.myCustomRedrawAccordingToNewPropsHandler = function (newProps) {
          newProps.handleExpression(global)
          faceapi.detectAllFaces(capture.id(), new faceapi.TinyFaceDetectorOptions()).withFaceExpressions().then((data) => {
            if (data[0] && data[0].expressions){
              setTimeout(() => newProps.handleExpression(data[0].expressions), 1500);
            }
          });
        }
    }
  };
