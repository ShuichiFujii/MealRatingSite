/**
 * home.js
 * index.html のセクションスライダー
 *
 * SECTION_DATA は Django テンプレートが埋め込む JSON:
 * {
 *   "morning":    [ {id, name, average_rating, image}, ... ],
 *   "afternoon":  [...],
 *   "evening":    [...],
 *   "recent":     [...],
 *   "top_rated":  [...],
 * }
 *
 * 各セクションは3件ずつ表示し、› / ‹ で次/前の3件へスライド。
 */

const PAGE_SIZE = 3;

document.querySelectorAll('.home-section').forEach(section => {
    const category = section.dataset.category;
    const items     = SECTION_DATA[category] || [];
    const grid      = section.querySelector('.section-grid');
    const prevBtn   = section.querySelector('.section-nav-btn.prev');
    const nextBtn   = section.querySelector('.section-nav-btn.next');
    const indicator = section.querySelector('.section-nav-indicator');

    // データが PAGE_SIZE 以下なら ‹ › 不要
    if (items.length <= PAGE_SIZE) {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
        indicator.style.display = 'none';
        return;
    }

    let page = 0; // 0-indexed
    const totalPages = Math.ceil(items.length / PAGE_SIZE);

    function cardHTML(item) {
        const imgPart = item.image
            ? `<img src="${item.image}" alt="${item.name}">`
            : `<div class="meal-card-no-image">No image</div>`;
        return `
            <a class="meal-card" href="/meal/${item.id}/">
                ${imgPart}
                <div class="meal-card-body">
                    <h3>${item.name}</h3>
                    <p>Rating: ${item.average_rating !== null ? Number(item.average_rating).toFixed(1) : '—'}</p>
                </div>
            </a>`;
    }

    function render(direction) {
        const slice = items.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);

        // アニメーション方向
        const outClass = direction === 'next' ? 'slide-out-left' : 'slide-out-right';
        const inClass  = direction === 'next' ? 'slide-in-right'  : 'slide-in-left';

        grid.classList.add(outClass);

        setTimeout(() => {
            grid.innerHTML = slice.map(cardHTML).join('');
            grid.classList.remove(outClass);
            grid.classList.add(inClass);
            // 次フレームで in クラスを外してトランジション完了
            requestAnimationFrame(() => {
                requestAnimationFrame(() => grid.classList.remove(inClass));
            });
        }, 180);

        // ボタン状態
        prevBtn.disabled = page === 0;
        nextBtn.disabled = page === totalPages - 1;

        // インジケーター（ドット）
        indicator.innerHTML = Array.from({ length: totalPages }, (_, i) =>
            `<span class="dot ${i === page ? 'active' : ''}"></span>`
        ).join('');
    }

    prevBtn.addEventListener('click', () => {
        if (page > 0) { page--; render('prev'); }
    });

    nextBtn.addEventListener('click', () => {
        if (page < totalPages - 1) { page++; render('next'); }
    });

    // 初期インジケーター描画
    render(null);
});