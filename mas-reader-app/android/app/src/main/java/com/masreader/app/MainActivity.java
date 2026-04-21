package com.masreader.app;

import android.os.Bundle;
import androidx.core.splashscreen.SplashScreen;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        SplashScreen.installSplashScreen(this);
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onPause() {
        super.onPause();
        try {
            this.bridge.getWebView().evaluateJavascript(
                "if(typeof matrixEngine!=='undefined'&&matrixEngine&&matrixEngine.stop){matrixEngine.stop();}" +
                "if(typeof bgEffectEngine!=='undefined'&&bgEffectEngine&&bgEffectEngine.stop){bgEffectEngine.stop();}",
                null
            );
        } catch (Exception e) {}
    }

    @Override
    public void onResume() {
        super.onResume();
        try {
            this.bridge.getWebView().evaluateJavascript(
                "if(typeof matrixEngine!=='undefined'&&matrixEngine&&matrixEngine.start){matrixEngine.start();}" +
                "if(typeof bgEffectEngine!=='undefined'&&bgEffectEngine&&bgEffectEngine.start){bgEffectEngine.start();}",
                null
            );
        } catch (Exception e) {}
    }
}
