<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rance 10 Battle System - Enhanced UI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #2a1810, #5c2d1a);
            height: 100vh;
            overflow: hidden;
            position: relative;
        }

        .battle-container {
            width: 100vw;
            height: 100vh;
            position: relative;
            display: flex;
            flex-direction: column;
        }

        /* Boss Area */
        .boss-area {
            flex: 1;
            background: linear-gradient(45deg, #8B0000, #DC143C);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .boss-area::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
            animation: float 10s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        .boss-placeholder {
            width: 300px;
            height: 200px;
            background: rgba(0,0,0,0.3);
            border: 3px solid #fff;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* HP Bars */
        .hp-container {
            height: 60px;
            display: flex;
            position: relative;
            background: rgba(0,0,0,0.8);
            border-top: 2px solid #444;
            border-bottom: 2px solid #444;
        }

        .hp-bar {
            flex: 1;
            position: relative;
            overflow: hidden;
        }

        .hp-enemy {
            background: linear-gradient(90deg, #8B0000, #DC143C);
            position: relative;
        }

        .hp-ally {
            background: linear-gradient(90deg, #1E90FF, #4169E1);
            position: relative;
        }

        .hp-fill {
            height: 100%;
            width: 75%;
            background: inherit;
            position: relative;
            transition: width 0.8s ease-out;
        }

        .hp-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s ease-in-out infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .hp-text {
            position: absolute;
            top: 50%;
            left: 20px;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            font-size: 18px;
        }

        .round-indicator {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: #FFD700;
            padding: 8px 16px;
            border-radius: 20px;
            border: 2px solid #FFD700;
            font-weight: bold;
            font-size: 14px;
        }

        /* AP System */
        .ap-container {
            height: 50px;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            border-bottom: 2px solid #444;
        }

        .ap-orb {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            border: 3px solid #FFD700;
            background: radial-gradient(circle, #FFD700, #FFA500);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: bold;
            font-size: 14px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .ap-orb.active {
            box-shadow: 0 0 15px #FFD700;
            animation: glow 1s ease-in-out infinite alternate;
        }

        .ap-orb.used {
            background: #333;
            border-color: #666;
            color: #888;
        }

        @keyframes glow {
            0% { box-shadow: 0 0 15px #FFD700; }
            100% { box-shadow: 0 0 25px #FFD700, 0 0 35px #FFD700; }
        }

        /* Characters Area */
        .characters-area {
            height: 280px;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
        }

        .characters-container {
            display: flex;
            gap: 30px;
            align-items: center;
            justify-content: center;
        }

        .character {
            width: 140px;
            height: 200px;
            position: relative;
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 15px;
            overflow: hidden;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            border: 3px solid transparent;
        }

        .character.hero {
            width: 160px;
            height: 220px;
            border-color: #FFD700;
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }

        .character:hover {
            transform: translateY(-10px) scale(1.05);
            border-color: #4CAF50;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
        }

        .character.hero:hover {
            transform: translateY(-10px) scale(1.15);
        }

        .character.cooldown {
            opacity: 0.5;
            filter: grayscale(100%);
            cursor: not-allowed;
        }

        .character.cooldown:hover {
            transform: none;
            border-color: transparent;
            box-shadow: none;
        }

        .character-portrait {
            width: 100%;
            height: 140px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 16px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            position: relative;
            overflow: hidden;
        }

        .character-portrait::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: rgba(255,255,255,0.5);
            transform: translateY(70px);
        }

        .character-info {
            padding: 10px;
            background: rgba(0,0,0,0.8);
            height: 60px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .character-name {
            color: #FFD700;
            font-weight: bold;
            font-size: 12px;
            margin-bottom: 3px;
        }

        .character-hp {
            color: #4CAF50;
            font-size: 11px;
        }

        .character-ap {
            position: absolute;
            top: 5px;
            right: 5px;
            background: rgba(0,0,0,0.8);
            color: #FFD700;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #FFD700;
        }

        .attack-zones {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 60px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .character:hover .attack-zones {
            opacity: 1;
        }

        .attack-zone {
            position: absolute;
            left: 0;
            right: 0;
            height: 50%;
            background: rgba(76, 175, 80, 0.3);
            border: 2px dashed #4CAF50;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }

        .attack-zone.top {
            top: 0;
        }

        .attack-zone.bottom {
            bottom: 0;
        }

        /* Control Buttons */
        .controls {
            height: 80px;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
        }

        .guard-button {
            background: linear-gradient(135deg, #3498db, #2980b9);
            border: 3px solid #2980b9;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .guard-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(52, 152, 219, 0.4);
            background: linear-gradient(135deg, #2980b9, #3498db);
        }

        .menu-button {
            background: linear-gradient(135deg, #95a5a6, #7f8c8d);
            border: 3px solid #7f8c8d;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .menu-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(127, 140, 141, 0.4);
        }

        .cooldown-timer {
            position: absolute;
            top: -10px;
            right: -10px;
            width: 30px;
            height: 30px;
            background: #e74c3c;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid white;
            animation: countdown 1s ease-in-out infinite;
        }

        @keyframes countdown {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        /* Hover Effects */
        .tooltip {
            position: absolute;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 12px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            white-space: nowrap;
            z-index: 1000;
        }

        .tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: rgba(0,0,0,0.9);
        }

        .character:hover .tooltip {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="battle-container">
        <!-- Boss Area -->
        <div class="boss-area">
            <div class="boss-placeholder">
                DEMON LORD BOSS
            </div>
        </div>

        <!-- HP Bars -->
        <div class="hp-container">
            <div class="hp-bar hp-enemy">
                <div class="hp-fill"></div>
                <div class="hp-text">Enemy HP: 2,448,177</div>
            </div>
            <div class="round-indicator">Round 18</div>
            <div class="hp-bar hp-ally">
                <div class="hp-fill"></div>
                <div class="hp-text">Ally HP: 3,307,542</div>
            </div>
        </div>

        <!-- AP System -->
        <div class="ap-container">
            <div class="ap-orb active">1</div>
            <div class="ap-orb active">2</div>
            <div class="ap-orb active">3</div>
            <div class="ap-orb active">4</div>
            <div class="ap-orb used">5</div>
            <div class="ap-orb used">6</div>
        </div>

        <!-- Characters -->
        <div class="characters-area">
            <div class="characters-container">
                <!-- Ally 1 -->
                <div class="character">
                    <div class="character-portrait">Ally 1</div>
                    <div class="character-info">
                        <div class="character-name">Mage Knight</div>
                        <div class="character-hp">132,245</div>
                    </div>
                    <div class="character-ap">2</div>
                    <div class="attack-zones">
                        <div class="attack-zone top">Power Strike</div>
                        <div class="attack-zone bottom">Magic Blast</div>
                    </div>
                    <div class="tooltip">Click upper half: Power Strike (2 AP)<br>Click lower half: Magic Blast (1 AP)</div>
                </div>

                <!-- Ally 2 -->
                <div class="character cooldown">
                    <div class="character-portrait">Ally 2</div>
                    <div class="character-info">
                        <div class="character-name">Assassin</div>
                        <div class="character-hp">126,236</div>
                    </div>
                    <div class="character-ap">0</div>
                    <div class="cooldown-timer">2</div>
                    <div class="tooltip">On cooldown - 2 rounds remaining</div>
                </div>

                <!-- Hero (Center) -->
                <div class="character hero">
                    <div class="character-portrait">HERO</div>
                    <div class="character-info">
                        <div class="character-name">Rance</div>
                        <div class="character-hp">167,787</div>
                    </div>
                    <div class="character-ap">4</div>
                    <div class="attack-zones">
                        <div class="attack-zone top">Brutal Strike</div>
                        <div class="attack-zone bottom">Special Move</div>
                    </div>
                    <div class="tooltip">Click upper half: Brutal Strike (3 AP)<br>Click lower half: Special Move (4 AP)</div>
                </div>

                <!-- Ally 3 -->
                <div class="character">
                    <div class="character-portrait">Ally 3</div>
                    <div class="character-info">
                        <div class="character-name">Healer</div>
                        <div class="character-hp">543,638</div>
                    </div>
                    <div class="character-ap">1</div>
                    <div class="attack-zones">
                        <div class="attack-zone top">Holy Light</div>
                        <div class="attack-zone bottom">Absorb Curse</div>
                    </div>
                    <div class="tooltip">Click upper half: Holy Light (1 AP)<br>Click lower half: Absorb Curse (0 AP)</div>
                </div>

                <!-- Ally 4 -->
                <div class="character">
                    <div class="character-portrait">Ally 4</div>
                    <div class="character-info">
                        <div class="character-name">Warrior</div>
                        <div class="character-hp">165,734</div>
                    </div>
                    <div class="character-ap">1</div>
                    <div class="attack-zones">
                        <div class="attack-zone top">Sword Slash</div>
                        <div class="attack-zone bottom">Shield Bash</div>
                    </div>
                    <div class="tooltip">Click upper half: Sword Slash (1 AP)<br>Click lower half: Shield Bash (1 AP)</div>
                </div>
            </div>
        </div>

        <!-- Controls -->
        <div class="controls">
            <button class="menu-button">MENU</button>
            <button class="guard-button">🛡️ GUARD (1 AP)</button>
        </div>
    </div>

    <script>
        // Add interactive behaviors
        document.querySelectorAll('.character:not(.cooldown)').forEach(char => {
            char.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const y = e.clientY - rect.top;
                const isUpperHalf = y < (rect.height - 60) / 2;

                // Add clicked effect
                this.style.transform = 'scale(0.95)';
                this.style.filter = 'brightness(1.2)';

                setTimeout(() => {
                    this.style.transform = '';
                    this.style.filter = '';

                    // Add to cooldown
                    this.classList.add('cooldown');
                    const timer = document.createElement('div');
                    timer.className = 'cooldown-timer';
                    timer.textContent = '3';
                    this.appendChild(timer);

                    // Simulate cooldown countdown
                    let count = 3;
                    const countdown = setInterval(() => {
                        count--;
                        timer.textContent = count;
                        if (count <= 0) {
                            clearInterval(countdown);
                            this.classList.remove('cooldown');
                            timer.remove();
                        }
                    }, 1000);
                }, 200);

                console.log(`${this.querySelector('.character-name').textContent} used ${isUpperHalf ? 'first' : 'second'} attack!`);
            });
        });

        // Guard button functionality
        document.querySelector('.guard-button').addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            this.style.background = 'linear-gradient(135deg, #27ae60, #2ecc71)';
            this.textContent = '🛡️ GUARDING...';

            setTimeout(() => {
                this.style.transform = '';
                this.style.background = '';
                this.textContent = '🛡️ GUARD (1 AP)';
            }, 1500);

            console.log('Guard activated!');
        });

        // Menu button
        document.querySelector('.menu-button').addEventListener('click', function() {
            alert('Menu opened!');
        });

        // Animate AP orbs
        setInterval(() => {
            document.querySelectorAll('.ap-orb.active').forEach((orb, index) => {
                setTimeout(() => {
                    orb.style.transform = 'scale(1.1)';
                    setTimeout(() => {
                        orb.style.transform = '';
                    }, 200);
                }, index * 100);
            });
        }, 3000);
    </script>
</body>
</html>
