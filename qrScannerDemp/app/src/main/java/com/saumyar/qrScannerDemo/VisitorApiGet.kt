package com.saumyar.qrScannerDemo

import io.reactivex.Observable
import kotlinx.android.synthetic.main.activity_main.*
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.Retrofit
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST



interface VisitorApiGet {

    @GET("api_getAllVisitors")
    fun getAllVisitors(): Observable<VisitorMODEL.Result>




    companion object {
        fun create(): com.saumyar.qrScannerDemo.VisitorApiGet {


            val retrofit = Retrofit.Builder()
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .addConverterFactory(GsonConverterFactory.create())
                .baseUrl("http://192.168.43.194:8080/")
                .build()

            return retrofit.create(VisitorApiGet::class.java)
        }
    }

}
