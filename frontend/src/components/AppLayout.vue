<template>
  <main class="app-shell" aria-label="gobang-python">
    <section class="play-surface" aria-label="棋局">
      <header class="topbar">
        <div class="title-group">
          <p class="eyebrow">
            <slot name="eyebrow" />
          </p>
          <h1>
            <slot name="title" />
          </h1>
        </div>
        <slot name="status" />
      </header>

      <div class="board-zone">
        <slot name="board" />
      </div>
    </section>

    <aside class="side-panel" aria-label="棋局控制">
      <slot name="panel" />
    </aside>
  </main>
</template>
