package com.saumyar.qrScannerDemo

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Window



class Splash_Screen : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash__screen)

        /***************************
        To hide action bar in splash screen
         ***************************/
        if (supportActionBar != null) {
            supportActionBar?.hide()
        }



        val background=object : Thread()
        {
            override fun run()
            {
                try{
                    //Keep Splash screen for 3sec
                    Thread.sleep(3000)
                    //Start android background service
                    val intent= Intent(baseContext,  MainActivity::class.java)
                    startActivity(intent)
                    /*finish the activity once the screen is displayed
                    so that on pressing back we will not go back to splash screen */
                    finish()


                }
                //catch if any exception occurs
                catch(e:Exception)
                {
                    e.printStackTrace()
                }
            }
        }
//it starts the thread named background
background.start()
    }


}


