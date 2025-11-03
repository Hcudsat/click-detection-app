import { useCallback, useState } from 'react';
import axios from 'axios';

const HEART_LIFETIME_MS = 1000;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000';

function App() {
  const [hearts, setHearts] = useState([]);

  const sendEvent = useCallback(
    async ({ x, y, timestamp }) => {
      try {
        await axios.post(
          `${API_BASE_URL}/api/click`,
          {
            x,
            y,
            t: timestamp,
          },
          {
            timeout: 3000,
          }
        );
      } catch (error) {
        console.error('Failed to send click event', error);
      }
    },
    []
  );

  const handleInteraction = useCallback(
    async (event) => {
      const target = event.currentTarget;
      const rect = target.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const timestamp = Date.now();

      const id = crypto.randomUUID();
      const heart = { id, x, y };
      setHearts((prev) => [...prev, heart]);
      setTimeout(() => {
        setHearts((prev) => prev.filter((item) => item.id !== id));
      }, HEART_LIFETIME_MS);

      await sendEvent({ x, y, timestamp });
    },
    [sendEvent]
  );

  const handleKeyDown = useCallback(
    (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        const syntheticEvent = {
          ...event,
          clientX: window.innerWidth / 2,
          clientY: window.innerHeight / 2,
          currentTarget: event.currentTarget,
        };
        handleInteraction(syntheticEvent);
      }
    },
    [handleInteraction]
  );

  return (
    <div
      className="app"
      onClick={handleInteraction}
      onKeyDown={handleKeyDown}
      role="button"
      tabIndex={0}
    >
      {hearts.map((heart) => (
        <span
          key={heart.id}
          className="heart"
          style={{ left: `${heart.x}px`, top: `${heart.y}px` }}
        >
          ❤️
        </span>
      ))}
      <div className="instructions">
        Click or press Enter/Space to send a heartbeat to the server.
      </div>
    </div>
  );
}

export default App;
