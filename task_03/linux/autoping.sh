  #!/bin/bash

  IP_PORT="$1"

  if [ "$#" -ne 1 ] || [ -z "$IP_PORT"  ]; then
      echo "IP address is not provided"
      exit 1
  fi

  log_file="${WORKSPACE}/autoping_${BUILD_NUMBER}.log"

  log() {
    echo -e "$IP_PORT" | tee -a "$log_file"
  }

  echo "$IP_PORT" | sed 's/,/\n/g' >"ip_ports.txt"
  i=1
  set +e

  while IFS= read -r line || [ -n "$line" ]; do

    TARGET=$(echo "$line" | cut -d ':' -f 1)
    PORT=$(echo "$line" | cut -d ':' -f 2)

    log "\n[$i] ====== Pinging $TARGET ======"

    if ping -4 -c 4 "$TARGET"; then
      log "Ping to $TARGET successful."
    else
      log "Ping to $TARGET failed."
    fi

    log "\n[$i] ====== Checking port $PORT on $TARGET ======"

    if nc -zv -w 30 "$TARGET" "$PORT"; then
      log "Port $PORT on $TARGET is open."
    else
      log "Port $PORT on $TARGET is closed."
    fi

    ((i++))

  done <"ip_ports.txt"
  set -e

  # -z, netcat sẽ không truyền dữ liệu nào qua kết nối.
  # -v verbose
  # -w 60 có nghĩa là netcat sẽ chờ tối đa 60 giây để kết nối đến cổng
