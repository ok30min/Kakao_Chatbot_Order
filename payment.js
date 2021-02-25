// 카카오페이로 결제하기 위한 코드
const axios = require('axios');


module.exports.payment = async ({ multiValueQueryStringParameters: params }) => {
  // get parmas
  const {
    item_name,      // 주문한 메뉴
    quantity,         // 주문 수량
    total_amount   // 총 결제 금액
  } = params;

  
  const vat_amount = 0;
  const tax_free_amount = 0;
  const approval_url = 'https:/example.com/approve';
  const fail_url = 'http://example.com/fail';
  const cancel_url = 'http://example.com/cancel';

  // set data
  const data = [
    'cid=TC0ONETIME',                                    // 테스트 결제를 위한 cid
    'partner_order_id=partner_order_id',
    'partner_user_id=partner_user_id',
    `item_name=${item_name}`,
    `quantity=${quantity}`,
    `total_amount=${total_amount}`,
    `vat_amount=${vat_amount}`,
    `tax_free_amount=${tax_free_amount}`,
    `approval_url=${approval_url}`,
    `fail_url=${fail_url}`,
    `cancel_url=${cancel_url}`
  ].join('&'); // encode data (application/x-www-form-urlencoded)

  // 카카오페이로 요청을 보내기 위한 Encoding
  const req = await axios.post('https://kapi.kakao.com/v1/payment/ready', data, {
    headers: {
      'Authorization': 'KakaoAK ************',                     // '******'에 Admin Key 추가
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });

  // PC로 결제하는 url을 받아온다. (모바일 결제 url : next_redirect_mobile_url)
  const pc_url = req.data.next_redirect_pc_url;     

  const response = {
    statusCode: 301, // redirect
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
      Location: pc_url
    },
    body: ''
  };

  return response;
};