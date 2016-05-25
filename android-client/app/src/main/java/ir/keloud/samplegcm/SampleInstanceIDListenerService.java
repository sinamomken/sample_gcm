package ir.keloud.samplegcm;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import com.google.android.gms.iid.InstanceIDListenerService;

public class SampleInstanceIDListenerService extends InstanceIDListenerService {
    public SampleInstanceIDListenerService() {
    }

    /**
     * Called if InstanceID token is updated. This may occur if the security of
     * the previous token had been compromised. This call is initiated by the
     * InstanceID provider.
     */
    // [START refresh_token]
    @Override
    public void onTokenRefresh(){
        Intent intent = new Intent(this, SampleRegistrationIntentService.class);
        startService(intent);
    }
    // [END refresh_token]
}
