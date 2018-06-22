===
// Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla.
//
// - Gummies tart bonbon muffin. Jelly chupa chups jelly-o tart dessert soufflé tiramisu. Apple pie pudding wafer. Sugar plum ice cream sesame snaps tootsie roll.
---
// Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
// ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
// parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec,
// pellentesque eu, pretium quis, sem. Nulla.
//
// - Gummies tart bonbon muffin. Jelly chupa chups jelly-o tart dessert
//   soufflé tiramisu. Apple pie pudding wafer. Sugar plum ice cream sesame
//   snaps tootsie roll.
===
/*
 * Jelly beans wafer topping sweet brownie. Croissant dragée cake sugar plum tootsie roll.
 * Icing croissant cotton candy croissant cotton candy pie.
 *
 * * Bullet list. Topping muffin cupcake cotton candy soufflé cake pie. Topping jelly jelly-o.
 * * Second item. Gingerbread chocolate gummies cake candy canes. Macaroon tart pudding bonbon macaroon jelly biscuit.
 */
---
/*
 * Jelly beans wafer topping sweet brownie. Croissant dragée cake sugar plum
 * tootsie roll. Icing croissant cotton candy croissant cotton candy pie.
 *
 * * Bullet list. Topping muffin cupcake cotton candy soufflé cake pie.
 *   Topping jelly jelly-o.
 * * Second item. Gingerbread chocolate gummies cake candy canes. Macaroon
 *   tart pudding bonbon macaroon jelly biscuit.
 */
===
/*
    <START>* Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    ** Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    + Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
      magnis dis parturient montes, nascetur ridiculus mus.
    ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et.<END>
*/
---
/*
    * Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
      ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
      dis parturient montes, nascetur ridiculus mus.
    ** Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean
       commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus
       et magnis dis parturient montes, nascetur ridiculus mus.
    + Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
      ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
      dis parturient montes, nascetur ridiculus mus. Lorem ipsum dolor sit
      amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.
      Aenean massa. Cum sociis natoque penatibus et magnis dis parturient
      montes, nascetur ridiculus mus.
    - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
      ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
      dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
      ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
      dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo
      ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis
      dis parturient montes, nascetur ridiculus mus. ipsum dolor sit amet,
      consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean
      massa. Cum sociis natoque penatibus et.
*/
===
/* C comment style
just writing stuff. */
---
/* C comment style just writing stuff.*/
===
/*
C comment style.
This probably shouldn't wrap with the opening tag, but it does. */
---
/* C comment style. This probably shouldn't wrap with the opening tag, but it
does. */
===
/*
<START>C comment style.
Works better when wrapping within the comment.<END> */
---
/*
C comment style. Works better when wrapping within the comment.*/
===
/**<START>
 * Comment with two stars. Cupcake ipsum dolor sit amet marzipan faworki.  Wafer I love croissant. Tart carrot cake pastry applicake lollipop I love cotton brownie.
 <END>*/
---
/**
 * Comment with two stars. Cupcake ipsum dolor sit amet marzipan faworki.
 * Wafer I love croissant. Tart carrot cake pastry applicake lollipop I love
 * cotton brownie.
 */
===
/**<START>
 * Sample function description.  Just in case the description is very long. Cupcake ipsum dolor sit amet marzipan faworki. Wafer I love croissant. Tart
 * carrot cake pastry applicake lollipop I love cotton brownie.
 * @param {string} paramname Multi-line parameter description (or any javadoc tag) should indent with 4 spaces.  Cupcake ipsum dolor sit amet marzipan faworki. Wafer I love croissant. Tart carrot cake pastry applicake lollipop I love cotton brownie.<END>
 */
---
/**
 * Sample function description.  Just in case the description is very long.
 * Cupcake ipsum dolor sit amet marzipan faworki. Wafer I love croissant. Tart
 * carrot cake pastry applicake lollipop I love cotton brownie.
 * @param {string} paramname Multi-line parameter description (or any javadoc
 *     tag) should indent with 4 spaces.  Cupcake ipsum dolor sit amet
 *     marzipan faworki. Wafer I love croissant. Tart carrot cake pastry
 *     applicake lollipop I love cotton brownie.
 */
