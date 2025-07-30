import os
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI
# from anthropic import Anthropic # Bỏ ghi chú nếu sử dụng Claude

def generate_asset(description, sample_url, output_format, ai_model, config):
    generated_content_path = f"./generated_asset.{output_format.lower()}"

    if ai_model.lower() == "openai":
        client = OpenAI(api_key=config['openai']['api_key'])
        model = config['openai']['model']
        
        # Tạo văn bản đơn giản để minh họa
        if output_format.lower() == "txt":
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Bạn là một trợ lý hữu ích tạo ra nội dung."},
                        {"role": "user", "content": f"Tạo một tài sản {output_format} dựa trên mô tả này: {description}. URL mẫu: {sample_url}"}
                    ]
                )
                generated_text = response.choices[0].message.content
                with open(generated_content_path, "w") as f:
                    f.write(generated_text)
                return generated_content_path
            except Exception as e:
                raise Exception(f"Tạo văn bản OpenAI thất bại: {e}")

        # Chỗ dành cho tạo hình ảnh (PNG, JPG, GIF)
        elif output_format.lower() in ["png", "jpg", "gif"]:
            try:
                # Trong một kịch bản thực tế, bạn sẽ gọi DALL-E hoặc các API tương tự ở đây
                # Để minh họa, hãy tạo một hình ảnh giả hoặc tải xuống một hình ảnh giữ chỗ
                print("Tạo hình ảnh OpenAI là một chức năng giữ chỗ. Đang tạo một hình ảnh giả.")
                img = Image.new('RGB', (200, 200), color = 'red')
                img.save(generated_content_path)
                return generated_content_path
            except Exception as e:
                raise Exception(f"Tạo hình ảnh OpenAI (giữ chỗ) thất bại: {e}")

        # Chỗ dành cho tạo âm thanh (MP3)
        elif output_format.lower() == "mp3":
            try:
                # Trong một kịch bản thực tế, bạn sẽ gọi API chuyển văn bản thành giọng nói ở đây
                print("Tạo âm thanh OpenAI là một chức năng giữ chỗ. Đang tạo một tệp âm thanh giả.")
                with open(generated_content_path, "wb") as f:
                    f.write(b'\x00\x01\x02\x03') # Nội dung âm thanh giả
                return generated_content_path
            except Exception as e:
                raise Exception(f"Tạo âm thanh OpenAI (giữ chỗ) thất bại: {e}")

    elif ai_model.lower() == "claude":
        # Bỏ ghi chú và cấu hình nếu sử dụng Claude của Anthropic
        # client = Anthropic(api_key=config['anthropic']['api_key'])
        # model = config['anthropic']['model']
        # try:
        #     response = client.messages.create(
        #         model=model,
        #         max_tokens=1024,
        #         messages=[
        #             {"role": "user", "content": f"Tạo một tài sản {output_format} dựa trên mô tả này: {description}. URL mẫu: {sample_url}"}
        #         ]
        #     )
        #     generated_text = response.content[0].text
        #     with open(generated_content_path, "w") as f:
        #         f.write(generated_text)
        #     return generated_content_path
        # except Exception as e:
        #     raise Exception(f"Tạo văn bản Claude thất bại: {e}")
        raise NotImplementedError("Tích hợp Claude chưa được triển khai đầy đủ.")

    else:
        raise ValueError(f"Mô hình AI không được hỗ trợ: {ai_model}")

    return None
