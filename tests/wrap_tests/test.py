Packages/Python/Python.sublime-syntax
===
def foo():
    """<START>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
    magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis,
    ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget,
    arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.

    :param foo: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
    <END>"""
    pass
---
def foo():
    """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean
    commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
    magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis,
    ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa
    quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget,
    arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
    Nullam dictum felis eu pede mollis pretium.

    :param foo: Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque
        penatibus et magnis dis parturient montes, nascetur ridiculus mus.
        Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem.
        Nulla consequat massa quis enim.
    """
    pass
===
# Comments.  Sweet danish gingerbread fruitcake caramels dessert apple pie sugar plum biscuit.
# Pie lollipop chocolate.
#
#     Indented. Chupa chups dessert donut muffin pie. Icing cotton candy lollipop dragée jelly-o chupa
#     chups brownie tiramisu. Fruitcake wafer croissant wafer gummi bears cake soufflé gummi bears pastry.
#
# # List item 1.
# # List item 2.  Cotton candy cake brownie cupcake jelly-o. Halvah marzipan cheesecake marshmallow.
# # List item 3.
# - Fruitcake tiramisu oat cake toffee. Chocolate cake cheesecake donut cheesecake powder toffee bear claw tart.
#
# > Blockquote. Jelly-o chocolate cake pie cotton candy candy croissant tiramisu. Jelly candy pastry cupcake cotton candy jelly-o soufflé. Danish fruitcake tiramisu chocolate cake chocolate cake carrot cake jelly beans biscuit sweet roll.
---
# Comments.  Sweet danish gingerbread fruitcake caramels dessert apple pie
# sugar plum biscuit. Pie lollipop chocolate.
#
#     Indented. Chupa chups dessert donut muffin pie. Icing cotton candy
#     lollipop dragée jelly-o chupa chups brownie tiramisu. Fruitcake wafer
#     croissant wafer gummi bears cake soufflé gummi bears pastry.
#
# # List item 1.
# # List item 2.  Cotton candy cake brownie cupcake jelly-o. Halvah marzipan
#   cheesecake marshmallow.
# # List item 3.
# - Fruitcake tiramisu oat cake toffee. Chocolate cake cheesecake donut
#   cheesecake powder toffee bear claw tart.
#
# > Blockquote. Jelly-o chocolate cake pie cotton candy candy croissant
# > tiramisu. Jelly candy pastry cupcake cotton candy jelly-o soufflé. Danish
# > fruitcake tiramisu chocolate cake chocolate cake carrot cake jelly beans
# > biscuit sweet roll.
