import * as faceapi from 'face-api.js';

const MODEL_URL = '/models'

export default async function () {
  console.log("hello")
  await Promise.all([
    faceapi.loadTinyFaceDetectorModel(MODEL_URL),
    // faceapi.loadSsdMobilenetv1Model(MODEL_URL),
    faceapi.loadFaceExpressionModel(MODEL_URL)
  ])

  // faceapi.detectAllFaces(capture.id()).withFaceExpressions().then((data) => {
  //   if (data[0] && data[0].expressions){
  //     //console.log(data[0].expressions)
  //     global.push(data[0].expressions)
  //   }
  //
  //     //howFaceDetectionData(data);
  // });

  self.addEventListener("message", e => {// eslint-disable-line no-restricted-globals
    // eslint-disable-line no-restricted-globals

    if (!e) return;
    console.log('Got message: ', e)

    const users = [];

    const userDetails = {
      name: "Jane Doe",
      email: "jane.doe@gmail.com",
      id: 1
    };

    for (let i = 0; i < 10000000; i++) {
      userDetails.id = i++;
      userDetails.dateJoined = Date.now();

      users.push(userDetails);
    }

    postMessage(users);
  });
};
