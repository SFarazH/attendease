import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAJAFZOlRw1YNDyOCV1Yv3W9EOURWgOboM",
  authDomain: "attendease-96875.firebaseapp.com",
  projectId: "attendease-96875",
  storageBucket: "attendease-96875.appspot.com",
  messagingSenderId: "80053895846",
  appId: "1:80053895846:web:06a0b8d00acf27e0ca6a67",
  measurementId: "G-P1KLBXZSHR",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
