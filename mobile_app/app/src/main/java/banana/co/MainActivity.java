package banana.co;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.RemoteException;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.altbeacon.beacon.Beacon;
import org.altbeacon.beacon.BeaconConsumer;
import org.altbeacon.beacon.BeaconManager;
import org.altbeacon.beacon.BeaconParser;
import org.altbeacon.beacon.Identifier;
import org.altbeacon.beacon.MonitorNotifier;
import org.altbeacon.beacon.RangeNotifier;
import org.altbeacon.beacon.Region;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class MainActivity extends AppCompatActivity implements BeaconConsumer {

    private static final int PERMISSION_REQUEST_COARSE_LOCATION = 1;
    protected static final String TAG = "RangingActivity";
    private static Region beaconRegion = new Region("myBeacons", null, null, null);

    private BeaconManager beaconManager;
    private BeaconsAdapter beaconsAdapter;

    private RecyclerView recyclerView;

    private List <Beacon> beaconsList= new ArrayList<Beacon>();
    private List <Beacon> beaconsListTEMP= new ArrayList<Beacon>();
    RequestQueue requestQueue;
    String beaconUUID ="";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        requestQueue= Volley.newRequestQueue(this);

        recyclerView = findViewById(R.id.recyclerView);

        showAlertforLocation();



        beaconsAdapter = new BeaconsAdapter(beaconsList, this);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(beaconsAdapter);




        beaconManager = BeaconManager.getInstanceForApplication(this);
        // To detect proprietary beacons, you must add a line like below corresponding to your beacon
        // type.  Do a web search for "setBeaconLayout" to get the proper expression.
        beaconManager.getBeaconParsers().add(new BeaconParser().
        setBeaconLayout("m:2-3=0215,i:4-19,i:20-21,i:22-23,p:24-24"));
        beaconManager.bind(this);



    }



    private void showAlertforLocation() {
        if(Build.VERSION.SDK_INT>= Build.VERSION_CODES.M){
            // android M znaci od sdk=23 do sdk=28, oneplus one mi je 27
            if (this.checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                final AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setTitle("This app needs location access");
                builder.setMessage("Please grant location access so this app can detect beacons.");
                builder.setPositiveButton(android.R.string.ok, null);
                builder.setOnDismissListener(new DialogInterface.OnDismissListener() {
                    @Override
                    public void onDismiss(DialogInterface dialog) {
                        requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION}, PERMISSION_REQUEST_COARSE_LOCATION);
                    }
                });
                builder.show();
            }
        }
    }


    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case PERMISSION_REQUEST_COARSE_LOCATION: {
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Log.d(TAG, "coarse location permission granted");
                } else {
                    final AlertDialog.Builder builder = new AlertDialog.Builder(this);
                    builder.setTitle("Functionality limited");
                    builder.setMessage("Since location access has not been granted, this app will not be able to discover beacons when in the background.");
                    builder.setPositiveButton(android.R.string.ok, null);
                    builder.setOnDismissListener(new DialogInterface.OnDismissListener() {

                        @Override
                        public void onDismiss(DialogInterface dialog) {
                        }

                    });
                    builder.show();
                }
                return;
            }
        }
    }


    @Override
    protected void onDestroy() {
        super.onDestroy();
        beaconManager.unbind(this);
    }

    @Override
    public void onBeaconServiceConnect() {

        beaconManager.removeAllRangeNotifiers();
        beaconManager.addRangeNotifier(new RangeNotifier() {
            @Override
            public void didRangeBeaconsInRegion(Collection<Beacon> beacons, Region region) {
                if (beacons.size() > 0) {
                    Log.i(TAG, "The first beacon I see is about "+beacons.iterator().next().getDistance()+" meters away.");
                    Log.i(TAG, "Beacons ID:  "+beacons.iterator().next().getId1().toString());

                    beaconsList.clear();
                    Log.i(TAG, "Beacons LIST:");
                    for (Beacon beacon: beacons){
                        beaconsList.add(beacon);
                        Log.i(TAG, "Beacons ID:  "+beacon.getId1().toString());
                        beaconUUID ="";
                        beaconUUID = beacon.getId1().toString();
                    }

                    beaconsAdapter.notifyDataSetChanged();

                    //String URL = "http://23.101.72.8:5000/api/beacon?UUID=fda50693-a4e2-4fb1-afcf-c6eb07647825&Major=5&Minor=6";

                    String URL ="http://23.101.72.8:5000/api/beacon?UUID=" +beaconUUID + "&Major=5&Minor=6";
                    // Poslati REST
                    JsonObjectRequest objectRequest = new JsonObjectRequest(
                            Request.Method.GET,
                            URL,
                            null,
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    String popust="";
                                    String voce="";
                                    try {
                                        popust = response.getString("Popust");
                                        voce = response.getString("Ime");
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }
                                    Log.i(TAG, "Request Response ------------ "+ popust);
                                    Log.i(TAG, URL);

                                    stopMonitoringBeacons();

                                    alert(voce, popust);

                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    Log.i(TAG, "Request ERROR Response ------------ "+ error);
                                    Log.i(TAG, URL);
                                }
                            }
                    );
                    requestQueue.add(objectRequest);
                }
                else{
                    //beaconsList.clear();
                    //beaconsAdapter.notifyDataSetChanged();
                }
            }

        });

        beaconManager.addMonitorNotifier(new MonitorNotifier() {
            @Override
            public void didEnterRegion(Region region) {
                Log.i(TAG, "I just saw an beacon for the first time!");
            }

            @Override
            public void didExitRegion(Region region) {
                Log.i(TAG, "I no longer see an beacon");
            }

            @Override
            public void didDetermineStateForRegion(int state, Region region) {
                Log.i(TAG, "I have just switched from seeing/not seeing beacons: "+state);
            }
        });


    }


    private void startMonitoringBeacons(){
        try {
            //beaconRegion = new Region("myBeacons", Identifier.parse("fda50693-a4e2-4fb1-afcf-c6eb07647825"), Identifier.parse("5"), Identifier.parse("6"));
            //beaconRegion = new Region("myBeacons", null, null, null);
            beaconManager.startRangingBeaconsInRegion(beaconRegion);
        } catch (RemoteException e) {    }
    }
    private void stopMonitoringBeacons(){
        try {
            beaconManager.stopRangingBeaconsInRegion(beaconRegion);
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }


    public void startMonitoringHandler(View view) {
        startMonitoringBeacons();
    }

    public void stopMonitoringHandler(View view) {
        stopMonitoringBeacons();
    }

    private void alert(String voce, String popust){
        DecimalFormat df = new DecimalFormat("0.00");
        float popustF = Float.parseFloat(popust);
        popustF = popustF * 100;
        AlertDialog dialog = new AlertDialog.Builder(MainActivity.this)
                .setTitle("Iskoristite popust %")
                .setMessage("Postovani, otkriven je novi popust na voce " + voce + " koji iznosi " + df.format(popustF) + "%. Iskoristi taj popust sada!")
                .setPositiveButton("Da", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                })
                .create();
        dialog.show();
    }
}