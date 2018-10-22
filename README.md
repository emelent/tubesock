# tubesock
Testing youtube-dl

{
  "name": "stringbean",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "start": "node node_modules/react-native/local-cli/cli.js start",
    "reset": "npm start -- --reset-cache",
    "prepare": "react-native bundle --dev false --platform android --entry-file index.android.js --bundle-output ./android/app/build/intermediates/assets/debug/index.android.bundle --assets-dest ./android/app/build/intermediates/res/merged/debug",
    "build": "npm run prepare && cd android && ./gradlew assembleDebug",
    "push": "code-push release-react stringbean android",
    "test": "jest"
  },
  "dependencies": {
    "mobile-center-analytics": "^0.5.0",
    "mobile-center-crashes": "^0.5.0",
    "react": "16.0.0-alpha.12",
    "react-native": "0.45.1",
    "react-native-code-push": "^2.1.0-beta",
    "react-native-linear-gradient": "^2.0.0",
    "react-native-shadow": "^1.1.2",
    "react-navigation": "^1.0.0-beta.11"
  },
  "devDependencies": {
    "babel-jest": "20.0.3",
    "babel-preset-react-native": "1.9.2",
    "eslint": "^4.0.0",
    "eslint-config-airbnb": "^15.0.1",
    "eslint-plugin-import": "^2.3.0",
    "eslint-plugin-jsx-a11y": "^5.0.3",
    "eslint-plugin-react": "^7.1.0",
    "jest": "20.0.4",
    "react-test-renderer": "16.0.0-alpha.12"
  },
  "jest": {
    "preset": "react-native"
  },
  "rnpm": {
    "assets": [
      "./assets/fonts"
    ]
  }
}
