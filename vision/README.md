Raspberry Pi vision scripts
===========================
* **For only streams (driver tryouts)**
	* Must use Raspbernie Sanders, as it has the correct camera serial number handling
	* python3 ~/vision/cscore_server.py
	* to view in browser with overlays open the html file `display_streams.html`
	* if you need to adjust the position of the red lines you'll have to know some basic html/css, just edit `display_streams.html`
* **For only GRIP**
	* probably best off just using Joe Piden if im not there
	* only plug in the gear camera
	* should start automatically
* **For both GRIP and streams**
	* Must use Raspbernie Sanders, as it has the correct camera serial number handling
	* Should start automatically
	* Stops grip for the gear camera after auto is over and switches to just streams
	* to view in browser with overlays open the html file `display_streams.html`
	* if you need to adjust the position of the red lines you'll have to know some basic html/css, just edit	
	* if you need to start it just do `sudo systemctl start vision.service`
