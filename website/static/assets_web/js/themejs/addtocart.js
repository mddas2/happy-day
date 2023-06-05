/* -------------------------------------------------------------------------------- /
	
	Magentech jQuery
	Created by Magentech
	v1.0 - 20.9.2016
	All rights reserved.
	
/ -------------------------------------------------------------------------------- */


	// Cart add remove functions
	var cart = {
		'add': function(product_id,product_name,product_image,quantity) {
			
			AddToCartAjax(product_id,quantity)
		
			addProductNotice('Product added to Cart', '<img src="'+product_image+'" alt="">', '<h3><a href="/view-cart/">'+product_name+'</a> added to <a href="#">shopping cart</a>!</h3>', 'success');
		}
	}

	var wishlist = {
		'add': function(product_id) {
			addProductNotice('Product added to Wishlist', '<img src="image/demo/shop/product/e11.jpg" alt="">', '<h3>You must <a href="#">login</a>  to save <a href="#">Apple Cinema 30"</a> to your <a href="#">wish list</a>!</h3>', 'success');
		}
	}
	var compare = {
		'add': function(product_id) {
			addProductNotice('Product added to compare', '<img src="image/demo/shop/product/e11.jpg" alt="">', '<h3>Success: You have added <a href="#">Apple Cinema 30"</a> to your <a href="#">product comparison</a>!</h3>', 'success');
		}
	}

	/* ---------------------------------------------------
		jGrowl – jQuery alerts and message box
	-------------------------------------------------- */
	function addProductNotice(title, thumb, text, type) {
		$.jGrowl.defaults.closer = false;
		//Stop jGrowl
		//$.jGrowl.defaults.sticky = true;
		var tpl = thumb + '<h3>'+text+'</h3>';
		$.jGrowl(tpl, {		
			life: 4000,
			header: title,
			speed: 'slow',
			theme: type
		});
	}

	function AddToCartAjax(product_id,quantity)
	{
		
		$.ajax({
			url: '/cart/', // URL of the server endpoint
			type: 'GET',
			dataType: 'json', // Expected data type of the response
			contentType: 'application/json', // Content type of the request payload
			data: {product_id:product_id,quantity:quantity}, // Convert your data to JSON format
			success: function(response) {
			  AppendToCart(response)			  
			},
			error: function(error) {
				
			  // Handle any errors that occurred during the request
			  console.error('Error:', error);
			}
		  });
		  
	}

	function AppendToCart(response){
		// Assuming the JSON response is stored in a variable named `response`
var cartData = response.cart_data;
console.log(cartData)

// Get the container element where you want to display the cart items
var container = $("#cart .dropdown-menu tbody");

// Clear the existing cart items
container.empty();

// Iterate over the cartData array using jQuery's $.each() function
$.each(cartData, function(index, cart) {
  // Create a table row for each cart item
		var row = $("<tr>");

		// Create and append the table cells with the cart item details
		var imageCell = $("<td>", { class: "text-center", style: "width:70px" });
		var imageLink = $("<a>", { href: "product.html" });
		var image = $("<img>", { src: cart.image, style: "width:70px", alt: cart.product_name, title: cart.product_name, class: "preview" });
		imageLink.append(image);
		imageCell.append(imageLink);
		row.append(imageCell);

		var nameCell = $("<td>", { class: "text-left" }).html('<a class="cart_product_name" href="product.html">' + cart.product_name + '</a>');
		row.append(nameCell);

		var quantityCell = $("<td>", { class: "text-center" }).text(cart.quantity);
		row.append(quantityCell);

		var priceCell = $("<td>", { class: "text-center" }).text("Rs." + cart.free_membership_price);
		row.append(priceCell);

		var editCell = $("<td>", { class: "text-right" }).html('<a href="product.html" class="fa fa-edit"></a>');
		row.append(editCell);

		var deleteCell = $("<td>", { class: "text-right" }).html('<a onclick="cart.remove(\'2\');" class="fa fa-times fa-delete"></a>');
		row.append(deleteCell);

		// Append the row to the container
		container.append(row);
		});

	}
