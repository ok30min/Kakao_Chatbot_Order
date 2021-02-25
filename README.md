# Kakao_Chatbot_Order

#### 카카오 i 오픈빌더를 사용하여 카카오톡 기반의 대화형 챗봇 인터페이스를 개발하였으며, 카카오페이를 사용하여 결제가 이루어질 수 있도록 하였습니다.   
#### 챗봇 서버와 카카오페이 서버를 연동시키기 위해 아마존에서 제공하는 서버리스 컴퓨텅 서비스인 AWS Lambda를 사용하였고, 고객 데이터 관리를 위해 DynamoDB를 사용했습니다.

## 개발 언어
  - Python
  - NodeJS
  
## 개발 플랫폼
  - AWS Lambda
  - Kakao i open builder
  - AWS DynamoDB

<hr/>

## 1. sign_up.py
#### 챗봇에서 사용자가 입력한 핸드폰 번호를 AWS Lambda에서 받아와 DynamoDB에 저장하는 코드입니다.

<hr/>

## 2. point_lookup.py
#### AWS Lambda에서 챗봇에서 사용자가 입력한 핸드폰 번호에 대한 정보를 입력받아 DynamoDB에 저장되어있는 사용자의 누적 포인트 값을 조회하는 코드입니다.

<hr/>

![image](https://user-images.githubusercontent.com/55127182/109089643-ece01a00-7754-11eb-80f7-820b9e5a5c95.png)
#### 1, 2번 코드가 작동하는 과정을 간단하게 나타낸 그림입니다.

<hr/>

#### 카카오 i 오픈 빌더 내에서 짜여진 주문 시나리오를 진행하면 아래와 같은 그림이 나옵니다.
![image](https://user-images.githubusercontent.com/55127182/109092429-dab4aa80-7759-11eb-9a6c-d68840f5b588.png)
#### 그림에서 "네 주문하겠습니다"를 선택하면 general_payment_preprocess.py가 연결되고, "포인트로 결제하기"를 선택하면 얼마나 사용할 것인지를 물어본 뒤, point_payment_preprocess.py로 연결됩니다.

<hr/>

## 3. general_payment_preprocess.py
#### 해당 코드는 결제가 이뤄지기 전, 총 결제 금액을 계산하기 위한 코드입니다.   
![image](https://user-images.githubusercontent.com/55127182/109089825-3f213b00-7755-11eb-947c-2211f297f33f.png)
#### 위 그림처럼 챗봇에서 사용자가 주문정보(메뉴 / 수량 / 핸드폰 번호)를 입력하게 되면 이에 따른 총 결제금액과 결제 후 적립될 포인트가 코드 내에서 계산되고, 계산된 값이 챗봇으로 사용자에게 전달됩니다.   
  - 총 결제 금액 = 가격 * 수량
  - 적립될 포인트 = 총 결제 금액 * 0.1    

![image](https://user-images.githubusercontent.com/55127182/109089953-83acd680-7755-11eb-84a2-5cef1520ccb3.png)
#### 이후 사용자는 위 그림과 같은 챗봇 메시지를 전달받게 되고, "결제하기" 버튼을 누르게 되면 payment.js 코드가 실행됩니다.

<hr/>

## 4. point_payment_preprocess.py
#### 해당 코드는 포인트를 사용하여 결제를 하기위해 작성된 코드이며 general_payment_preprocess.py와 비슷한 구성을 띄고 있습니다.   
![image](https://user-images.githubusercontent.com/55127182/109091160-988a6980-7757-11eb-8eff-4036b60ceb10.png)
#### 차이점은 사용자가 입력한 핸드폰 번호를 DynamoDB에서 조회하여 누적된 포인트 값을 불러온다. 이후 사용할 만큼의 포인트를 차감하고 최종 결제 금액을 챗봇으로 사용자에게 전달합니다.
  - 총 결제 금액 = 가격 * 수량
  - 최종 결제 금액 = 총 결제금액 - 사용할 포인트     

![image](https://user-images.githubusercontent.com/55127182/109091090-7f81b880-7757-11eb-9670-1ce16223815c.png)
#### 이후 사용자는 위 그림과 같은 챗봇 메시지를 전달받게 되고, "결제하기" 버튼을 누르게 되면 payment.js 코드가 실행됩니다.

<hr/>

## 5. payment.js
#### 해당 코드는 사용자가 챗봇에서 최종적으로 결제를 승인했을 때, 실행되는 코드입니다.   
![image](https://user-images.githubusercontent.com/55127182/109090522-6debe100-7756-11eb-89a1-e8228eb8e2fa.png)
#### 위 그림처럼 카카오페이에 주문 정보를 넘겨주고, 테스트 결제 URL을 실행시키면 아래와 같은 결제 창이 뜹니다.
![image](https://user-images.githubusercontent.com/55127182/109091010-4fd2b080-7757-11eb-9f79-2d3cd0d42d58.png)
#### 이 창에서 QR코드에 연결된 링크를 통하면 카카오페이를 이용한 테스트 결제가 진행됩니다.

<hr/>

## 6. 챗봇 주문 시스템 
![image](https://user-images.githubusercontent.com/55127182/109091410-12baee00-7758-11eb-912d-e3d4e53b6663.png)
#### 전체 주문 시스템을 요약한 그림입니다. 그리고 이 과정은 다음과 같습니다.      
  #### 1. 사용자가 주문 파라미터 입력 챗봇 시나리오에 따라 입력한다.     

      i) 사용자가 챗봇에 들어가 “주문하기” 버튼을 선택한다.   
      ii) 사용자가 원하는 메뉴와 수량을 선택한다.   
      iii) 사용자가 전화번호를 입력한다.   
      

  #### 2. 결제 방식을 선택한다.   
  
      i) 일반 결제와 포인트 결제 중 하나를 선택   
      
  #### 3. AWS Lambda에 저장된 코드를 통해 결제 방식에 따른 금액이 계산된다. 이와 더불어 사용자의 핸드폰 번호를 이용해 적립된 포인트를 DynamoDB에서 조회해 Background에 저장해놓는다.   
  #### 4. 챗봇으로 주문서 전송 후 사용자가 최종적으로 결제를 승인한다.   
  #### 5. 최종 주문 정보가 AWS Lambda로 전달되어 카카오페이에 맞는 형식으로 데이터가 변환된다. 이와 더불어 결제 방식에 따라 조회했던 포인트에 누적 혹은, 차감을 진행한다.   
  #### 6. 카카오페이 서버로 주문정보가 전달되면 카카오페이 시스템에 따라 결제가 진행된다.   
  #### 7. 카카오페이로부터 결제 완료 메시지가 사용자에게 전달된다.   
  #### 8. 카페에 방문하여 주문한 커피를 받는다.   


