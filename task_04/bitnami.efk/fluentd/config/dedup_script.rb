@@cache ||= {}

def filter(tag, time, record)
  # Kiểm tra nếu trường `msg` tồn tại
  log_key = record["message"]["msg"]

  Fluent::Engine.log.info("record[\"msg\"]: #{log_key}")

  # Kiểm tra log trùng lặp
  if @@cache[log_key]
    # Ghi log khi phát hiện trùng lặp
    Fluent::Engine.log.info("Duplicate log detected: #{log_key}")
    nil # Bỏ qua log trùng lặp
  else
    # Thêm vào cache và giới hạn kích thước
    @@cache[log_key] = true
    @@cache.shift if @@cache.size > 1000
    record
  end
end
