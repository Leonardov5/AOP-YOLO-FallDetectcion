from ultralytics import YOLO
import cv2
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime
import logging

logging.getLogger('ultralytics').setLevel(logging.WARNING)

class FallDetectionSystem:
    def __init__(self, model_path="models/fallDetection.pt"):
        self.model = YOLO(model_path)

        self.model.verbose = False
        self.fall_start_time = None
        self.fall_detected = False
        self.email_sent = False
        self.fall_threshold = 10  # Tempo limite em segundos
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "aopyolo@gmail.com"
        self.sender_password = "wqkjdcqjnojmxqib"
        self.recipient_email = "5leonardovieira55@gmail.com"
        
    def send_email_notification(self, image_path=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = "🚨 ALERTA: Queda Detetada!"
            
            timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            body = f"""
            ALERTA DE EMERGÊNCIA!
            
            Uma queda foi detetada e a pessoa permaneceu caída por mais de {self.fall_threshold} segundos.
            
            Detalhes:
            - Hora: {timestamp}
            - Estado: Requer atenção imediata
            
            Por favor, verifique a situação imediatamente.
            
            Sistema de Monitorização Automática
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-Disposition', 'attachment', filename='queda_detetada.jpg')
                    msg.attach(image)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            print(f"✅ Email de alerta enviado com sucesso para {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {str(e)}")
            return False
    
    def save_frame(self, frame, results, filename="queda_detetada.jpg"):
        try:
            annotated_frame = results[0].plot()
            cv2.imwrite(filename, annotated_frame)
            return filename
        except:
            return None
    
    def process_frame(self, frame):
        results = self.model.predict(frame, verbose=False)
        fall_detected_in_frame = False
        
        if results[0].boxes is not None:
            for box in results[0].boxes:
                conf = box.conf.cpu().numpy()[0]
                cls = int(box.cls.cpu().numpy()[0])
                class_name = self.model.names[cls]
                
                if class_name == "Fall-Detected" and conf > 0.5:
                    fall_detected_in_frame = True
                    break
        
        current_time = time.time()
        
        if fall_detected_in_frame:
            if not self.fall_detected:
                self.fall_detected = True
                self.fall_start_time = current_time
                self.email_sent = False
                print(f"⚠️  Queda detetada! A iniciar contagem de tempo...")
            
            time_fallen = current_time - self.fall_start_time
            
            if time_fallen >= self.fall_threshold and not self.email_sent:
                print(f"🚨 ALERTA: Pessoa caída à {time_fallen:.1f} segundos!")
                
                image_path = self.save_frame(frame, results)
                
                if self.send_email_notification(image_path):
                    self.email_sent = True
                
            status_text = f"Queda detetada: {time_fallen:.1f}s"
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                       
        else:
            if self.fall_detected:
                print("✅ Pessoa levantou-se.")
                self.fall_detected = False
                self.fall_start_time = None
                self.email_sent = False
        
        return results
    
    def run_camera(self, source=0):
        cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            print("❌ Erro: Não foi possível abrir a câmera")
            return
        
        print("📹 Sistema de deteção de queda iniciado...")
        print("Pressione 'q' para sair")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            results = self.process_frame(frame)
            
            annotated_frame = results[0].plot()
            
            cv2.imshow('Deteção de Queda', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def run_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Erro: Não foi possível abrir o vídeo {video_path}")
            return
        
        print(f"📹 A processar vídeo: {video_path}")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            results = self.process_frame(frame)
            
            annotated_frame = results[0].plot()
            
            cv2.imshow('Deteção de Queda', annotated_frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    
    fall_system = FallDetectionSystem("models/fallDetection.pt")

    try:
        fall_system.run_camera(0)
       
        # fall_system.run_video("video3.mp4")
        
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido.")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")