// Minimal Android Client (Kotlin)
// This is pseudocode showing the device-side logic

package com.taxidooh.mvp

import android.app.Activity
import android.os.Bundle
import android.widget.ImageView
import kotlinx.coroutines.*
import okhttp3.*
import com.bumptech.glide.Glide
import org.json.JSONObject

class FullscreenAdActivity : Activity() {

    private val SERVER_URL = "https://your-backend.com" // Configure this
    private val DEVICE_ID = "taxi_001" // Unique per tablet
    private val POLL_INTERVAL = 60_000L // 60 seconds

    private lateinit var imageView: ImageView
    private var currentImageUrl: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Fullscreen setup
        window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_FULLSCREEN
        actionBar?.hide()

        imageView = ImageView(this)
        imageView.scaleType = ImageView.ScaleType.FIT_CENTER
        setContentView(imageView)

        // Start background jobs
        startContentPolling()
        startHeartbeat()
    }

    private fun startContentPolling() {
        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                try {
                    checkForNewContent()
                } catch (e: Exception) {
                    // Log error, continue polling
                }
                delay(POLL_INTERVAL)
            }
        }
    }

    private suspend fun checkForNewContent() {
        val client = OkHttpClient()
        val request = Request.Builder()
            .url("$SERVER_URL/content/$DEVICE_ID")
            .build()

        client.newCall(request).execute().use { response ->
            if (response.isSuccessful) {
                val json = JSONObject(response.body!!.string())
                val images = json.getJSONArray("images")

                if (images.length() > 0) {
                    val newUrl = images.getString(0)

                    // Only update if content changed
                    if (newUrl != currentImageUrl) {
                        currentImageUrl = newUrl
                        updateDisplay(newUrl)
                    }
                }
            }
        }
    }

    private suspend fun updateDisplay(imageUrl: String) {
        withContext(Dispatchers.Main) {
            // Use Glide to load and cache images
            Glide.with(this@FullscreenAdActivity)
                .load(imageUrl)
                .into(imageView)
        }
    }

    private fun startHeartbeat() {
        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                try {
                    sendHeartbeat()
                } catch (e: Exception) {
                    // Log error, continue
                }
                delay(60_000L) // Every 60 seconds
            }
        }
    }

    private suspend fun sendHeartbeat() {
        val client = OkHttpClient()

        // Get GPS location (simplified)
        val location = getLastKnownLocation()

        val json = JSONObject().apply {
            put("device_id", DEVICE_ID)
            put("latitude", location?.latitude)
            put("longitude", location?.longitude)
        }

        val body = RequestBody.create(
            MediaType.parse("application/json"),
            json.toString()
        )

        val request = Request.Builder()
            .url("$SERVER_URL/heartbeat")
            .post(body)
            .build()

        client.newCall(request).execute()
    }
}

// That's it. Entire Android app in ~100 lines.
// No complex state management, no frameworks, just HTTP polling.
