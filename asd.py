delivery = Delivery(
            address="123 Main St",
            comments="Leave on doorstep"
            )
        try:
            db.session.add(delivery)
            db.session.commit()
            flash("Delivery created successfully.","success")
        except Exception as e:
            flash("Error creating delivery: {}".format(str(e)),"error")
            return redirect(url_for("all_dishes"))

#  
def confirmed_delivery():
    if request.method == "POST":
        delivery = Delivery(
            address =  request.form["delivery_address"],
            comments = request.form["comments"],
            phone_for_delivery = request.form["phone_number"]
        )
        try:
            db.session.add(delivery)
            db.session.commit()

            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if cart:
                cart.delivery_id = delivery.id # adding the delivery_id to the already existing cart object
                db.session.commit() # updating cart

            flash("Your order was created successfully","success")
            return render_template("one_delivery.html")
        
        except Exception as e:
            flash("Error creating cart: {}".format(str(e)),"error")
            return render_template("one_cart.html") 

    flash("There was a problem with creating your order.","error")
    return render_template("one_cart.html")