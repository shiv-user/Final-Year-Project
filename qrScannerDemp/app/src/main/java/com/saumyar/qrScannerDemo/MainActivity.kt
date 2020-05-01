package com.saumyar.qrScannerDemo

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.google.zxing.integration.android.IntentIntegrator
import kotlinx.android.synthetic.main.activity_main.*
import android.widget.Toast
import android.content.Intent
import android.view.View
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.disposables.Disposable
import io.reactivex.schedulers.Schedulers
import retrofit2.Call
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.Retrofit
import retrofit2.http.Body
import retrofit2.http.POST
import com.google.android.gms.tasks.Task
import retrofit2.Callback
import retrofit2.Response


class MainActivity : AppCompatActivity() {
   /*******************************************
  Declaration of nullable string xmlParse and baseUrl and a disposable variable
  Note:
  i) As in kotlin we can't make string null so we have to declare them nullable
  ii) Variables are declared disposable because after the system initiate the
   view (activity or fragment).
   The subscription start and then you decided to go back or initiate another
   view while the subscription still executed and didn't finish its job,
   this means that it's still in the memory that will cause a memory leak.
   So you have to call dispose method to unsubscribe.
  ********************************************/
    var xmlParse : String? = null
    var baseUrl: String? = "http://192.168.43.62:8000"
    private var disposable: Disposable? = null





    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        /**************************
        On Clicking Button "Camera icon" it will open the camera and start scanning
         **************************/

        btn_scan.setOnClickListener {
            val scanner = IntentIntegrator(this)
            scanner.initiateScan()
        }



        /**********************
        On Clicking "Submit" button:
        i) it will convert url entered into string
        NOte: url entered is of the server/system/network????? on which the backend is running
        ii) it will call the post api function
         ***********************/

        submit.setOnClickListener {

            if((url.text.toString().length<4))
                baseUrl = "http://192.168.43.62:8000"
            else
                baseUrl = (url.text.toString())

            testPostJsonByPojo()
            Toast.makeText(this,"Submitted", Toast.LENGTH_LONG).show()
        }



    }
// Function to set variables value after scan

    fun setValuesAfterScan (){

        var string = xmlParse as String


    /**************************
        if data extracted from QR Code is not null
        then we perform String manipulation such that
        data can be stored in the form we need it

     Here we are parsing the xml data into String
    inorder to fill the entries in Android application

     if the QR scanned is not of adhaar card it will show exception
                *******************************/

        if(xmlParse != null) {
            try {
                var nameSub = string.substring((string.indexOf("name") + 6))
                name.setText(nameSub.substring(0, nameSub.indexOf("\"")))
                var genderSub = string.substring((string.indexOf("gender") + 8), (string.indexOf("gender") + 9))
                gender.setText(genderSub)
                var subAddress =  string.substring((string.indexOf("co=") + 4), (string.indexOf("pc") - 1))
                subAddress = subAddress.replace("po=","post office : ")
                subAddress = subAddress.replace("dist=","District : ")
                subAddress = subAddress.replace("=","",true)
                subAddress = subAddress.replace("im","",true)
                subAddress = subAddress.replace("vtc","\n")
                subAddress = subAddress.replace("\""," ")
                address.setText( subAddress.substring(0,99))
                dob.setText(string.substring((string.indexOf("dob") + 5), (string.indexOf("dob") + 15)).replace("/","-"))

                pincode.setText(string.substring((string.indexOf("pc") + 4), (string.indexOf("pc") + 10)))
                uid.setText(string.substring((string.indexOf("uid") + 5), (string.indexOf("uid") + 17)))
            }
            /*************************
             3
             */


            catch (e : Exception)
            {
                Toast.makeText(this,"Only Aadhar Supported!!!", Toast.LENGTH_LONG).show()
            }

        }
    }




    /****************************************
      this is the callback function of the initiate scan function call
     ***************************************/
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        val result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)


        /*
       checking result is not null
         */
        if (result != null) {
            if (result.contents == null) {
                Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show()
            }

            /***********************************
             If the data is not equal to null set the values
             after scan by using string manipulation function
             setValueAfterScan()
             ***********************************/
            else {

                xmlParse = result.contents.toString()

                setValuesAfterScan()
            }
        }


        else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }





    /**************************
      Interface for retrofit
     **************************/
    interface VisitorApiPost {
        @POST("user/")
        fun createvisitor(@Body visitor: VisitorMODEL.VisitorPost): Call<VisitorMODEL.VisitorPost>
    }



    fun testPostJsonByPojo() {

        /************************
          if no url is entered by user set this "http://192.168.43.200:8080/" url as default
         ***********************/
        if(baseUrl == null)
        {
            baseUrl = "http://192.168.43.62:8000"
        }
        /**************************
         Retrofit builder object
         **************************/
        val retrofit = Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        //Toast.makeText(this, VisitorMODEL.VisitorPost(url.text.toString()), Toast.LENGTH_LONG).show()
        /**************************
        It will provide the retrofit instance
         **************************/
        val SendVisitor = retrofit.create(VisitorApiPost::class.java)

        /**************************
        Create a vistor by creating an object of VisitorMODEL.VisitorPost class and initalizing with aadhar values
         **************************/

        val visitor= VisitorMODEL.VisitorPost(name.text.toString(),uid.text.toString(),gender.text.toString(),address.text.toString(),dob.text.toString(),pincode.text.toString(),url.text.toString())

        //Toast.makeText(this, visitor.toString() , Toast.LENGTH_LONG).show()
        /**************************
        Creating a call with the visitor object
         **************************/
        val call = SendVisitor.createvisitor(visitor)

        /**************************
        sending aysnc post request
         **************************/
        call.enqueue(object : Callback<VisitorMODEL.VisitorPost>{

            /**************************
            call back function when we have a response
             **************************/
            override fun onResponse(
                call: Call<VisitorMODEL.VisitorPost>,
                response: Response<VisitorMODEL.VisitorPost>
            ) {
                Toast.makeText(applicationContext, response.toString(), Toast.LENGTH_SHORT).show()

            }
            /**************************
            call back function in case of error
             **************************/
            override fun onFailure(call: Call<VisitorMODEL.VisitorPost>, t: Throwable) {
                Toast.makeText(applicationContext, t.toString(), Toast.LENGTH_SHORT).show()
            }

        })
    }




   /********************************************
    after the system initiate the
    view (activity or fragment).
    The subscription start and then you decided to go back or initiate another
    view while the subscription still executed and didn't finish its job,
    this means that it's still in the memory that will cause a memory leak.
    So you have to call dispose method to unsubscribe.
    **********************************************/
    override fun onPause() {
        super.onPause()
        disposable?.dispose()
    }
}
