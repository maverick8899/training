POST login
curl 'http://wsl.local:9001/api/v1/login' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.9,vi;q=0.8' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/json' \
    -H 'Cookie: lang=en-US; i_like_gitea=54a7dc8bc0d82b5e; _csrf=ZWJ9svkw-zdZgLNoDKlCGLJM1486MTczMTMxNDg2NzA0NDA1NjEwNw' \
    -H 'Origin: http://wsl.local:9001' \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
    --data-raw '{"accessKey":"admin","secretKey":"Root2003@"}' \
    --insecure

POST SA credentials
curl 'http://wsl.local:9001/api/v1/service-account-credentials' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.9,vi;q=0.8' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/json' \
    -H 'Cookie: lang=en-US; i_like_gitea=54a7dc8bc0d82b5e; _csrf=ZWJ9svkw-zdZgLNoDKlCGLJM1486MTczMTMxNDg2NzA0NDA1NjEwNw; token=ACwTQIqXHPLddXHMZDOQsQfr/PBes3isq/AhmiMXmB3nYAqlN/oupSrCKlcWxTZQZoTgDtVu1bK3nlrlupBezcWdD4AaQSgAhjj4M3GRsniQB8Lw82/gnmj7xHbidZeIGzlBXiZq4GpjaKX8ulWm+xWLGT3aL9zeIuO9AcHVABYMQic+HG7GkOOSFlXowH7Xam8S1DgPTDLNNmVeBcV4mBBpFJhkPwg1PSnZKSYdZbENMW6gflpWjiAj7Xu2/cnzKiWJ1piG1ol7SgQjl2a4afcs9Y+6YrSVNsDThwXT5GkM2FWTNcMC/UCVibNQzcIfMUhKk+bYsZzdFMEF8mBPpPVaRJ0XZrRpKLUXh8bcSeyafGIMYuTE08CZ5JvEnku84VOgJ0MwiawBAtwXHO0y4NPabOyiN8aqgFZr10VH3m4Wa7H8UyaDwjOzy+s2KNqDZJz816KAajvdwcmtGkiV3RoDBkEDVCMtpDMAU9E3yV1pjSpg+t9a5HBuBFzMcugbryzv3yxPjAk36ALuL46TlGSCqM9DYlR4oI7h9RCKdKw=' \
    -H 'Origin: http://wsl.local:9001' \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
    --data-raw '{"policy":"","accessKey":"LPrtk3s63XrXcVTEv3aS","secretKey":"j4zI2WBoy4wvOxuCLigMxFQ7Jw84HvqjjobmAbZf","description":"","comment":"","name":"","expiry":null}' \
    --insecure
