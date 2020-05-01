package com.saumyar.qrScannerDemo

object VisitorMODEL {
    //class that will be used to store all data that is required for post request
    data class VisitorPost( val name: String, val uid: String, val gender: String, val address:  String, val dob:  String, val pincode: String, val url: String)
}