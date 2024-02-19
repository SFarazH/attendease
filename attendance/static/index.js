import { initializeApp } from "firebase/app";
import { getAnalytics, getAnalytics } from "firebase/analytics";

console.log("firebase");
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
const analytics = getAnalytics();

logEvent(analytics, "notification_received");

// const analytics = getAnalytics();
// logEvent(analytics, "notification_received");
