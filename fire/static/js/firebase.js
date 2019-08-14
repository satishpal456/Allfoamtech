import firebase from 'firebase';
import 'firebase/firestore';

const firebaseConfig = {
  apiKey: 'AIzaSyCC6uEdeE_3L6KKgBePW8n77sPNir5c4Bw',
  authDomain: 'sprayer-loyalty-a3d4a.firebaseapp.com',
  databaseURL: 'https://sprayer-loyalty-a3d4a.firebaseio.com',
  projectId: 'sprayer-loyalty-a3d4a',
  storageBucket: 'sprayer-loyalty-a3d4a.appspot.com',
  messagingSenderId: '624993131038',
  appId: '1:624993131038:web:5e7292485eb5d29b',
};

export default (!firebase.apps.length
  ? firebase.initializeApp(firebaseConfig).firestore()
  : firebase.app().firestore());
