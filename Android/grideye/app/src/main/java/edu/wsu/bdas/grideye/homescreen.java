package edu.wsu.bdas.grideye;

import android.app.Activity;
import android.os.Bundle;
import android.content.Context;
import android.os.Handler;
import android.view.Menu;
import android.view.MenuItem;
import android.hardware.usb.*;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.hoho.android.usbserial.driver.*;
import com.hoho.android.usbserial.util.*;


import org.w3c.dom.Text;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;



public class homescreen extends Activity {

    public UsbSerialDriver driver;
    @Override
    protected void onCreate(Bundle savedInstanceState)  {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_homescreen);
        final TextView txt = (TextView) findViewById(R.id.bufferTemp);
        Button connectBtn = (Button) findViewById(R.id.connectBtn);
        Button dcBtn = (Button) findViewById(R.id.dcBtn);

        View.OnClickListener btnCnt = new View.OnClickListener() {
            @Override
            public void onClick(View v)  {
                // change text of the TextView (tvOut)
                UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);

// Find the first available driver.
                driver = UsbSerialProber.acquire(manager);

                if (driver != null) {


                    try {
                        driver.open();
                        driver.setBaudRate(115200);
                        driver.write(new String("*").getBytes(),1);
                        byte[] buffer = new byte[133];
                        driver.read(buffer, 133);
                        txt.append(buffer.toString());
                        driver.close();
                    } catch (IOException e) {
                        txt.setText("ERROR");
                    } finally {

                    }
                }
            }
        };

        View.OnClickListener dcCn = new View.OnClickListener() {
            @Override
            public void onClick(View v)  {
                // change text of the TextView (tvOut)
                UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);

// Find the first available driver.
                driver = UsbSerialProber.acquire(manager);

                if (driver != null) {


                    try {
                        driver.open();
                        driver.setBaudRate(115200);
                        driver.write(new String("~").getBytes(),1);
                        driver.close();
                        txt.setText("Disconnected!");
                    } catch (IOException e) {
                        // Deal with error.
                    } finally {
                    }
                }
            }
        };


        connectBtn.setOnClickListener(btnCnt);
        dcBtn.setOnClickListener(dcCn);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.homescreen, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
