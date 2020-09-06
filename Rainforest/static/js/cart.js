console.log("cart");

var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'action:', action)
		console.log('USER:', user)

		if (user === 'AnonymousUser'){
			addCookieItem(productId, action)
		} else { 
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')
		// url for post data.
		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
			// Show response to console.
		   return response.json();
		})
		.then((data) => {
			// Refresh page.
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')
	// If user clicks the up botton on product, add another
	// product to cart.
	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1};

		} else {
			cart[productId]['quantity'] += 1;
		}
	}
	// If user clicks the down button on product, remove
	// the product from the cart.
	if (action == 'remove'){
		cart[productId]['quantity'] -= 1;
		// This should nevershouldn't be reached because the product
		// shouldn't be rendered when quantity is 0.
		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart);
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	// TBH a REST api would've been a better way to do this but I just
	// want to see the update.
	location.reload()
}