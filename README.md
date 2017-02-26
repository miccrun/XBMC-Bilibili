# Bilibili Plugin for Kodi

## Usage
Make a HTTP request to
```
http://<kodi_ip>/jsonrpc?request={"jsonrpc":"2.0","method":"Addons.ExecuteAddon","params":{"addonid":"plugin.video.bilibili","params":["/video/<av_id>/<page_id>/"]},"id":1}
```

Change your kodi_ip, av_id, and page_id
