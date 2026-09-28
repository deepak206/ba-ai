function StatusBadge({ status }) {
    return (
      <span className="inline-flex rounded-full bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400 ring-1 ring-blue-500/20">
        {status}
      </span>
    );
  }
  
  export default StatusBadge;