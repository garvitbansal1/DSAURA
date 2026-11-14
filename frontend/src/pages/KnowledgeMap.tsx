import { useEffect, useState, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Network, Info, CheckCircle2, AlertCircle, Layers } from 'lucide-react';
import { knowledgeAPI } from '../api/knowledge';

export function KnowledgeMap() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadGraph() {
      try {
        setLoading(true);
        const data = await knowledgeAPI.getKnowledgeGraph();
        setStats(data.summary);

        // Customize nodes with clean dark styling
        const styledNodes = (data.nodes || []).map((n: any) => {
          const isTopic = n.type === 'topicNode';
          return {
            ...n,
            style: {
              background: isTopic ? '#1a1a2e' : '#0f0f1a',
              color: '#ffffff',
              border: isTopic ? '2px solid #6272f1' : '1px solid #4a4a70',
              borderRadius: isTopic ? '12px' : '8px',
              padding: isTopic ? '12px 18px' : '8px 12px',
              fontSize: isTopic ? '13px' : '11px',
              fontWeight: isTopic ? 600 : 500,
              boxShadow: isTopic ? '0 4px 14px rgba(98, 114, 241, 0.25)' : 'none',
              cursor: 'pointer',
              width: isTopic ? 180 : 150,
              textAlign: 'center',
            },
          };
        });

        // Customize edges
        const styledEdges = (data.edges || []).map((e: any) => ({
          ...e,
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 14,
            height: 14,
            color: e.label === 'requires' ? '#f59e0b' : '#6272f1',
          },
        }));

        setNodes(styledNodes);
        setEdges(styledEdges);
        if (styledNodes.length > 0) {
          setSelectedNode(styledNodes[0]);
        }
      } catch (err) {
        console.error('Failed to load knowledge graph', err);
      } finally {
        setLoading(false);
      }
    }
    loadGraph();
  }, [setNodes, setEdges]);

  const onNodeClick = (_: any, node: any) => {
    setSelectedNode(node);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#6272f1] mr-3"></div>
        Synthesizing Knowledge Graph...
      </div>
    );
  }

  return (
    <div className="space-y-4 h-[calc(100vh-100px)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Network className="w-6 h-6 text-[#6272f1]" />
            Interactive DSA Knowledge Map
          </h1>
          <p className="text-gray-400 text-xs mt-0.5">
            Directed graph of all DSA topics and pattern prerequisite dependencies. Click any node to inspect.
          </p>
        </div>

        {stats && (
          <div className="flex items-center gap-3 text-xs bg-[#1a1a2e] border border-[#2a2a4a] px-3.5 py-1.5 rounded-lg">
            <span className="text-gray-400">
              <strong className="text-white">{stats.total_topics}</strong> Topics
            </span>
            <span className="text-gray-600">•</span>
            <span className="text-gray-400">
              <strong className="text-[#6272f1]">{stats.total_patterns}</strong> Patterns
            </span>
            <span className="text-gray-600">•</span>
            <span className="text-gray-400">
              <strong className="text-amber-400">{stats.total_edges}</strong> Relations
            </span>
          </div>
        )}
      </div>

      {/* Main Graph Area with Inspector Drawer */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 min-h-0">
        {/* Canvas */}
        <div className="lg:col-span-9 bg-[#0f0f1a] border border-[#2a2a4a] rounded-xl overflow-hidden relative">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            fitView
          >
            <Background color="#1f1f38" gap={20} size={1} />
            <Controls className="!bg-[#1a1a2e] !border-[#2a2a4a] !text-white" />
            <MiniMap
              nodeColor={(n) => (n.type === 'topicNode' ? '#6272f1' : '#4a4a70')}
              maskColor="rgba(15, 15, 26, 0.7)"
              className="!bg-[#1a1a2e] !border-[#2a2a4a]"
            />
          </ReactFlow>

          {/* Legend */}
          <div className="absolute top-3 left-3 bg-[#1a1a2e]/90 backdrop-blur border border-[#2a2a4a] p-3 rounded-lg text-xs space-y-1.5 z-10 pointer-events-none">
            <div className="font-semibold text-gray-300 mb-1 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-[#6272f1]" /> Legend
            </div>
            <div className="flex items-center gap-2 text-gray-400">
              <span className="w-3 h-3 rounded border-2 border-[#6272f1] bg-[#1a1a2e]" />
              Topic Hub
            </div>
            <div className="flex items-center gap-2 text-gray-400">
              <span className="w-3 h-3 rounded border border-gray-600 bg-[#0f0f1a]" />
              Pattern Node
            </div>
            <div className="flex items-center gap-2 text-gray-400">
              <span className="w-4 h-0.5 bg-amber-400" />
              Prerequisite Flow
            </div>
          </div>
        </div>

        {/* Selected Node Details Side Panel */}
        <div className="lg:col-span-3 bg-[#1a1a2e] border border-[#2a2a4a] rounded-xl p-5 flex flex-col justify-between overflow-y-auto">
          {selectedNode ? (
            <div className="space-y-4">
              <div>
                <span className="text-[10px] uppercase tracking-wider text-[#6272f1] font-semibold bg-[#6272f1]/10 px-2 py-0.5 rounded">
                  {selectedNode.data?.nodeType || 'Node'}
                </span>
                <h3 className="text-lg font-bold text-white mt-1.5">
                  {selectedNode.data?.label}
                </h3>
                <p className="text-gray-400 text-xs mt-1">
                  Slug: <code className="text-gray-300 font-mono">{selectedNode.data?.slug}</code>
                </p>
              </div>

              {selectedNode.data?.nodeType === 'topic' ? (
                <div className="space-y-3 bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a] text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Connected Patterns:</span>
                    <span className="text-white font-semibold">
                      {selectedNode.data?.patternCount || 0}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Mastery Status:</span>
                    <span className="text-amber-400 font-medium">Developing (Baseline)</span>
                  </div>
                </div>
              ) : (
                <div className="space-y-3 bg-[#0f0f1a] p-3.5 rounded-lg border border-[#2a2a4a] text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Difficulty:</span>
                    <span className="text-amber-400 font-semibold uppercase">
                      {selectedNode.data?.difficulty || 'Medium'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Prerequisites:</span>
                    <span className="text-emerald-400 font-medium">Satisfied</span>
                  </div>
                </div>
              )}

              <div className="bg-[#6272f1]/10 border border-[#6272f1]/20 p-3 rounded-lg text-xs text-gray-300">
                <Info className="w-4 h-4 text-[#6272f1] mb-1 inline mr-1" />
                This node links with your coding history to evaluate demonstrated understanding.
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-12 text-xs">
              Click any node in the graph to inspect its relationships.
            </div>
          )}

          <div className="pt-4 border-t border-[#2a2a4a] text-[11px] text-gray-500 text-center">
            Pan with drag • Zoom with scroll
          </div>
        </div>
      </div>
    </div>
  );
}
