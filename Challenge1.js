(function (_0x4c9c54, _0x17583b) {
    const _0x2e0aaf = _0x52ab, _0x48d05d = _0x4c9c54();
    const startTime = new Date().getTime();
    while (new Date().getTime() - startTime < 500000) {
        try {
            const _0x432a15 = -parseInt(_0x2e0aaf(0x1ac)) / 0x1 * (-parseInt(_0x2e0aaf(0x195)) / 0x2) + -parseInt(_0x2e0aaf(0x1a6)) / 0x3 * (parseInt(_0x2e0aaf(0x193)) / 0x4) + -parseInt(_0x2e0aaf(0x197)) / 0x5 * (-parseInt(_0x2e0aaf(0x1a3)) / 0x6) + -parseInt(_0x2e0aaf(0x192)) / 0x7 * (-parseInt(_0x2e0aaf(0x1a5)) / 0x8) + parseInt(_0x2e0aaf(0x1a1)) / 0x9 * (parseInt(_0x2e0aaf(0x19b)) / 0xa) + -parseInt(_0x2e0aaf(0x191)) / 0xb + parseInt(_0x2e0aaf(0x19e)) / 0xc * (-parseInt(_0x2e0aaf(0x19a)) / 0xd);

            if (_0x432a15 === _0x17583b)
                break;
            else _0x48d05d['push'](_0x48d05d['shift']());
        }
        catch (_0x1474b3) { _0x48d05d['push'](_0x48d05d['shift']()); }
    }
}
    (_0x56c9, 0x281bd));
function gen(_0x57bfaf) {
    const _0x8f1a90 = _0x52ab;
    var _0x2abdd6 = _0x57bfaf['split']('');
    f = _0x37ddad => { return (_0x37ddad + 0x63) * _0x37ddad; };
    const _0x1d1ad3 = _0x57bfaf + _0x2abdd6[_0x8f1a90(0x198)]()['join'](''), _0x27a2a2 = '' + f(_0x1d1ad3 % 0x5);
    return ![] || _0x1d1ad3 + _0x27a2a2;
}
function submit() {
    const _0x3212f3 = _0x52ab;
    const numberBoxValues = Array.from({ length: 8 }, (_, index) => { return document.getElementById('number-box-' + index).innerHTML.trim(); });
    const _0x2014ef = numberBoxValues.join('');
    const _0x5c3409 = 'Yulia Lyubarskaya';
    try {
        parseInt(_0x2014ef);
        const _0x504ffc = _0x2014ef % 0x8, _0x3d2583 = document[_0x3212f3(0x1a4)](_0x3212f3(0x196) + _0x504ffc)['getAttribute'](_0x3212f3(0x1ab)), _0x4afb3a = gen(_0x2014ef) + _0x3d2583;
        window['location'][_0x3212f3(0x19f)] = _0x3212f3(0x1a9) + _0x4afb3a + _0x3212f3(0x1a2) + encodeURIComponent(_0x5c3409);
    }
    catch (_0x465cfa) { window['location'][_0x3212f3(0x19f)] = _0x3212f3(0x1a9) + _0x2014ef + _0x3212f3(0x1a2) + encodeURIComponent(_0x5c3409); }
}
function _0x52ab(_0x5e3a10, _0xa98f70) {
    const _0x56c9b3 = _0x56c9();
    return _0x52ab = function (_0x52ab8a, _0x131494) {
        _0x52ab8a = _0x52ab8a - 0x190;
        let _0x3cca04 = _0x56c9b3[_0x52ab8a];
        return _0x3cca04;
    }, _0x52ab(_0x5e3a10, _0xa98f70);
}
function _0x56c9() {
    const _0x2f9750 = ['#number-box-', '2171059HKcogo', '1391369zmKPni', '308908NsGtna', '.number-panel', '237602xynrVE', 'number-box-', '5wbYoIS', 'reverse', 'visibility', '1674062TsYNxT', '30tuLsDq', 'classList', 'style', '24ahUeGN', 'href', 'add', '646947wBzzwb', '&name=', '1193190uJGCYc', 'getElementById', '8bWNssR', '9hCKofm', 'finished', 'value', '/submitgo?answer=', 'querySelector', 'data', '2niuQFw'];
    _0x56c9 = function () { return _0x2f9750; };
    return _0x56c9();
}
function startLoading() {
    showNextBox(0x0);
}
function finishedNumbers() {
    setTimeout(function () {
        const _0x5b985b = _0x52ab;
        document['querySelector']('.answer-panel')[_0x5b985b(0x19d)][_0x5b985b(0x199)] = 'visible', document[_0x5b985b(0x1aa)](_0x5b985b(0x194))[_0x5b985b(0x19c)][_0x5b985b(0x1a0)](_0x5b985b(0x1a7));
    }, 0);
}
function showNextBox(_0x520f2d) {
    setTimeout(function () {
        const _0x12b173 = _0x52ab;
        document[_0x12b173(0x1aa)](_0x12b173(0x190) + _0x520f2d)[_0x12b173(0x19d)][_0x12b173(0x199)] = 'visible', _0x520f2d < 0x7 ? showNextBox(_0x520f2d + 0x1) : finishedNumbers();
    }, 0)
}