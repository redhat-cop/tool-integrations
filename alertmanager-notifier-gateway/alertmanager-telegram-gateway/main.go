/*
Comments: Implemented based on https://core.telegram.org/bots.
*/
package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/prometheus/alertmanager/template"
	log "github.com/sirupsen/logrus"
)

const telegramAPIUrl = "https://api.telegram.org"

//Set logger to stdout
func init() {
	log.SetFormatter(&log.TextFormatter{
		DisableColors: true,
		FullTimestamp: true,
	})
	log.SetOutput(os.Stdout)
	log.SetLevel(log.InfoLevel)

}

func webhook(w http.ResponseWriter, r *http.Request) {
	//Defer the Close() method until this function return.
	defer r.Body.Close()
	radd := r.RemoteAddr
	rmtd := r.Method
	ruri := r.RequestURI
	hres := http.StatusText(http.StatusMethodNotAllowed)

	//Extract and decode basic auth to be reused in the POST URL.
	ah := r.Header.Get("Authorization")
	b64t := strings.Split(ah, " ")[1]
	ab, err := base64.StdEncoding.DecodeString(b64t)
	if err != nil {
		log.Fatal(err)
	}
	a := string(ab)

	switch r.Method {
	case "POST":
		//Initialized empty payload struct from alertmanager template Data struct.
		payload := template.Data{}

		//Telegram Bot ChatID declaration
		cid := os.Getenv("ChatID")
		if cid == "" {
			log.Fatal("ChatID environment setting not found!")
		}

		//Parse the request body and load into payload struct template.
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			http.Error(w, "HTTP Bad Request: Unable to parse received payload", http.StatusBadRequest)
			return
		}
		for _, alert := range payload.Alerts {
			//fmt.Println(alert)
			//Extract required info and assigned each var
			ls := alert.Labels["alertname"]
			fp := alert.Fingerprint
			at := alert.StartsAt.String()
			as := alert.Status
			am := alert.Annotations["message"]
			sl := alert.Labels["severity"]

			//Build up a data string
			resp := "AlertName=" + ls + "\nSeverity=" + sl + "\nAlertStartsAt=" + at + "\nAlertStatus=" + as + "\nAlertMessage=" + am

			//Create a value data that server will understand to be posted.
			postData := url.Values{}
			postData.Set("text", resp)
			postData.Set("chat_id", cid)

			// It looks like this https://api/bot_token/sendMessage
			tg := telegramAPIUrl + "/" + a + "/sendMessage"

			//Create new HTTP Post, and post data with proper authorization and Content-Type header.
			client := &http.Client{}
			request, err := http.NewRequest("POST", tg, bytes.NewBufferString(postData.Encode()))
			request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
			if err != nil {
				log.Fatal(err)
			}

			defer request.Body.Close()

			log.WithFields(log.Fields{
				"ClientAddress":    radd,
				"AlertFingerprint": fp,
				"AlertName":        ls,
				"RemoteHTTPUrl":    telegramAPIUrl,
			}).Info("Posting message.")

			s, err := client.Do(request)
			if err != nil {
				log.Fatal(err)
			}

			log.WithFields(log.Fields{
				"ServerHTTPUrl":      telegramAPIUrl,
				"ServerHTTPResponse": s.StatusCode,
			}).Info("Response received.")
			return
		}

	default:
		http.Error(w, "Method not Allowed", http.StatusMethodNotAllowed)
		log.WithFields(log.Fields{
			"ClientAddress": radd,
			"HTTPUri":       ruri,
			"HTTPResponse":  hres,
			"HTTPMethod":    rmtd,
		}).Info("Error handling request")
		return

	}

}

//Implement a handler for healthz
func healthz(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	radd := r.RemoteAddr
	rmtd := r.Method
	ruri := r.RequestURI
	hres := http.StatusText(http.StatusMethodNotAllowed)

	if r.URL.Path != "/healthz" {
		http.Error(w, "Not Found", http.StatusNotFound)
		return
	}
	switch r.Method {

	case "GET":
		w.Write([]byte("I`m ready\n"))
		return

	default:
		http.Error(w, "Method not Allowed", http.StatusMethodNotAllowed)
		log.WithFields(log.Fields{
			"ClientAddress": radd,
			"HTTPUri":       ruri,
			"HTTPResponse":  hres,
			"HTTPMethod":    rmtd,
		}).Info("Error handling request")
		return
	}
}

//All the magic starts here
func main() {

	http.HandleFunc("/healthz", healthz)
	log.Info("Initialized /healthz handler")

	http.HandleFunc("/webhook", webhook)
	log.Info("Initialized /webhook handler")

	if os.Getenv("insecure") == "false" {
		if os.Getenv("tlscert") == "" {
			log.Fatal("Missing TLS cert as tlscert env.")
		}

		if os.Getenv("tlskey") == "" {
			log.Fatal("Missing TLS key tlskey env.")
		}

		log.Info("Serving TLS at 0.0.0.0:8443")
		err := http.ListenAndServeTLS(":8443", os.Getenv("tlscert"), os.Getenv("tlskey"), nil)
		if err != nil {
			log.Fatal(err)
		}
	} else {
		log.Info("Serving at 0.0.0.0:8080")
		err := http.ListenAndServe(":8080", nil)
		if err != nil {
			log.Fatal(err)
		}
	}
}
