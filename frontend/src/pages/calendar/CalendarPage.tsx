import React, { useEffect, useState } from "react";
import { Calendar as CalendarIcon, Clock, MapPin } from "lucide-react";
import { api } from "../../services/api";
import { CalendarEvent } from "../../types";

export const CalendarPage: React.FC = () => {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    api.getCalendarEvents().then(res => setEvents(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Meeting Calendar</h1>
        <p className="text-xs text-slate-500">Upcoming client engagements, demos, and syncs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {events.map(ev => (
          <div key={ev.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{ev.title}</h4>
            <div className="text-[11px] text-slate-500 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5" />
              <span>{new Date(ev.start_time).toLocaleString()}</span>
            </div>
            {ev.location && (
              <div className="text-[11px] text-slate-500 flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5" />
                <span>{ev.location}</span>
              </div>
            )}
          </div>
        ))}
        {events.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No scheduled meetings today.</div>}
      </div>
    </div>
  );
};
