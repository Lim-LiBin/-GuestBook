
var countdownInterval; // 카운트다운 인터벌을 관리하는 변수
let client = null; // MQTT 클라이언트 변수
const CLIENT_ID = "client-"+Math.floor((1+Math.random())*0x100000000000).toString(16) // 랜덤 클라이언트 ID 생성
let canvas; // Canvas 변수
let context; // Canvas 2D 컨텍스트 변수

// 카운트다운 시작 함수
function startCountdown() {
    var countdownElement = document.getElementById('countdown');

    // 3, 2, 1, 스마일 텍스트를 1초 간격으로 표시
    var countdown = 3;
    countdownInterval = setInterval(function () {
        if (countdown > 0) {
            countdownElement.innerText = countdown;
            countdown--;
        } else {
            countdownElement.innerText = '스마일~';
            clearInterval(countdownInterval); // 카운트다운 종료
        }
    }, 1000);
}

// 폼 제출 함수
function submitForm() {
    clearInterval(countdownInterval); // 카운트다운이 종료되지 않았다면 종료
    console.log("Form submitted");
    document.forms['takePictureForm'].submit(); // 폼 제출
}

// 웹 페이지 로드 시 실행되는 함수
window.addEventListener("load", function () {
    // 현재 페이지의 URL을 문자열로 가져옴
    let broker = new String(document.location);

    // URL에서 프로토콜 및 포트를 추출하여 MQTT 브로커의 IP 주소 설정
    ip = (broker.split("//"))[1];
    ip = (ip.split(":"))[0];

    // MQTT 클라이언트 초기화
    client = new Paho.MQTT.Client(ip, 9001, CLIENT_ID);

    // MQTT 메시지 도착 시 호출될 콜백 함수 설정
    client.onMessageArrived = onMessageArrived;

    // MQTT 브로커에 연결
    client.connect({
        onSuccess: onConnect,
    });

    // Canvas 요소 및 2D 컨텍스트 초기화 
    canvas = document.getElementById("myCanvas");
    context = canvas.getContext("2d");
});

// MQTT 연결 시 실행되는 함수
function onConnect() {
    client.subscribe("dis"); // "dis" 토픽 구독
    client.subscribe("temp"); // "temp" 토픽 구독
    client.subscribe("image"); // "image" 토픽 구독
}

// MQTT 메시지 수신 시 실행되는 함수
function onMessageArrived(msg) {
    console.log("onMessageArrived: " + msg.destinationName + "-" + msg.payloadString);

    if (msg.destinationName === "dis") { // 메시지 토픽이 "dis"라면
        console.log("Distance message received");
        // HTML 문서에서 "dis_message" 요소를 찾아서 현재 거리를 표시
        document.getElementById("dis_message").innerHTML = "거리: " + msg.payloadString + "cm";
    } else if (msg.destinationName === "temp") { // 메시지 토픽이 "temp"라면
        console.log("Temperature message received");
        // HTML 문서에서 "temp_message" 요소를 찾아서 현재 온도를 표시
        document.getElementById("temp_message").innerHTML = "온도: " + msg.payloadString + "°"; // 출력
    } else if (msg.destinationName == "image") { // 메시지 토픽이 "image"라면
        console.log("Image received");
        drawImage(msg.payloadString); // Base64 문자열을 그리는 함수 호출
    }
}

// Canvas에 이미지를 그리는 함수
function drawImage(base64String) {
    // Canvas에 이미지 그리기
    var img = new Image();
    img.onload = function () {
        context.clearRect(0, 0, canvas.width, canvas.height); // Canvas 초기화
        context.drawImage(img, 0, 0, canvas.width, canvas.height); // 이미지 그리기
    };
    img.src = "data:image/jpeg;base64," + base64String; // Base64 문자열을 이미지로 변환하여 할당
}
