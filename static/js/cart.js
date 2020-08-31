var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var productPrice = this.dataset.price
		var productName = this.dataset.name
		var productImage = this.dataset.image
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action, 'Price:', productPrice)
//should just use cart data
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action, productPrice, productName, productImage)
		}else{
			updateUserOrder(productId, action, productPrice, productName, productImage)
		}
	})
}
//logged in update db --bad
function updateUserOrder(productId, action, productPrice){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'productPrice':productPrice})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
//cookies for not login --good
function addCookieItem(productId, action, productPrice, productName, productImage){
	console.log('User is not authenticated')
//clicking add to cart and adding data to the cart
	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'productId':productId,'productPrice':productPrice, 'quantity':1, 'productName':productName, 'productImage':productImage}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}