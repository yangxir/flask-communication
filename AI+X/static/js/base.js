const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let w = canvas.width = window.innerWidth;
let h = canvas.height = window.innerHeight;

let lines = [];

class Line {
	constructor() {
		this.x = Math.random() * w;
		this.y = Math.random() * h;
		this.vx = Math.random() * 2 - 1;
		this.vy = Math.random() * 2 - 1;
		this.size = Math.random() * 2 + 1;
	}
	draw() {
		ctx.beginPath();
		ctx.moveTo(this.x, this.y);
		ctx.lineTo(this.x + this.vx * 10, this.y + this.vy * 10);
		ctx.lineWidth = this.size;
		ctx.strokeStyle = "#ffffff";
		ctx.stroke();
	}
	update() {
		this.x += this.vx;
		this.y += this.vy;
		if (this.x < 0 || this.x > w) {
			this.vx *= -1;
		}
		if (this.y < 0 || this.y > h) {
			this.vy *= -1;
		}
	}
}

function loop() {
	ctx.clearRect(0, 0, w, h);
	lines.forEach(line => {
		line.draw();
		line.update();
	});
	requestAnimationFrame(loop);
}

function init() {
	lines = [];
	for (let i = 0; i < 2; i++) {
		lines.push(new Line());
	}
	loop();
}

window.addEventListener("resize", () => {
	w = canvas.width = window.innerWidth;
	h = canvas.height = window.innerHeight;
	init();
});

init();
