const form = document.getElementById('employeeForm');
const resultContainer = document.getElementById('resultContainer');

form.addEventListener('submit', function(e) {
  e.preventDefault();
  const id = document.getElementById('idInput').value;

  // // new url (code thêm thôi - không ảnh hưởng đến ajax) - thay đổi url của một trang mà không request lại trang 
  // var url = window.location.href;
  // var newUrl = url.slice(0, -1) + 'id'
  // window.history.pushState(null, null, newUrl);
  // console.log(newUrl);
  // // new url  

  fetch('/test-ajax', {
  // Nhắt lại : fetch('test-ajax', { . nếu ghi như thế này thì ajax sẽ cộng dồn url hiện tại trên trang vs fetch đó 
  // sẽ là http://localhost:8000/abc.../test-ajax
  // Còn nếu ghi fetch('/test-ajax', { thì sẽ là http://localhost:8000/test-ajax 
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: new URLSearchParams({id: id}),
  })
  .then(response => response.json())
  .then(data => {
    const employee = data;
    const html = `
      <p>ID: ${employee.id}</p>
      <p>Email: ${employee.email}</p>
      <p>Contact: ${employee.contact}</p>
    `;
    resultContainer.innerHTML = html;
  })
  .catch(error => console.log(error));
});
