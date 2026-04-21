import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.masreader.app',
  appName: 'Mas.reader',
  webDir: 'www',
  server: {
    androidScheme: 'https'
  }
};

export default config;
