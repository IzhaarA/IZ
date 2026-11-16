/* track what visitors do in the shop (product opened, category, search, add to basket, checkout, order) */
(function () {
  var T = function (o) { try { window.mkTrack && window.mkTrack(o); } catch (e) {} };
  var _op = openProduct; openProduct = function (id) { try { var p = byId[id]; T({ e: 'product', p: ((p && (p.p || p).name) || id) + ' · ' + id }); } catch (e) {} return _op.apply(this, arguments); };
  var last = ''; var _go = go; go = function (v) {
    try {
      if (v === 'shop' && state.q && state.q.trim()) T({ e: 'search', q: state.q.trim() });
      else if (v === 'shop' && state.cat !== 'all' && state.cat !== last) T({ e: 'cat', p: COLLECTIONS[state.cat] ? COLLECTIONS[state.cat].label : state.cat });
      if (v === 'shop') last = state.cat; else if (v === 'home') last = '';
      if (v === 'checkout' && state.cart.length) T({ e: 'checkout' });
    } catch (e) {}
    return _go.apply(this, arguments);
  };
  var _add = addToCart; addToCart = function (id) { try { var r = byId[id]; T({ e: 'add', p: (r && r.p ? r.p.name : id) }); } catch (e) {} return _add.apply(this, arguments); };
  var _po = placeOrder; placeOrder = async function () { var r = await _po.apply(this, arguments);
    try { if (document.getElementById('done').classList.contains('open')) T({ e: 'order' }); } catch (e) {} return r; };
})();
