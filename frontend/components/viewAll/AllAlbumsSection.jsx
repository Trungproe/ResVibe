"use client";

import Image from "next/image";
import Link from "next/link";
import { Music4 } from "lucide-react";

export default function AllAlbumSection({ albums }) {
  // Kiểm tra nếu không có album nào
  if (!albums || albums.length === 0) {
    return <p className="text-white">No albums found.</p>;
  }

  return (
    // Hiển thị danh sách album dưới dạng lưới
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      {albums.map((album) => (
        <Link
          key={album.id}
          href={`/album/${album.id}`}
          className="group bg-[#2A2A2A]/60 hover:bg-[#39FF14]/10 rounded-xl border border-[#39FF14]/10 hover:border-[#39FF14]/40 shadow-md hover:shadow-[#39FF14]/30 transition-all duration-300 overflow-hidden"
        >
          {/* Ảnh bìa album */}
          <div className="relative w-full h-44 overflow-hidden">
            <Image
              src={album.cover_art || "/placeholder.svg"}
              alt={album.title}
              fill
              className="object-cover rounded-t-xl group-hover:scale-105 transition-transform duration-500"
            />

            {/* Lớp phủ mờ phía trên ảnh */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-t-xl" />

            {/* Icon trạng thái góc phải trên */}
            <div className="absolute top-2 right-2 z-10">
              <div className="w-9 h-9 flex items-center justify-center rounded-full bg-black/60 transition-all group-hover:bg-[#39FF14]/20">
                <Music4
                  size={18}
                  className="text-white group-hover:text-[#00FFCC] transition-colors"
                />
              </div>
            </div>
          </div>

          {/* Tiêu đề và năm phát hành album */}
          <div className="p-4 text-center space-y-1">
            <h4 className="text-white font-semibold text-base truncate">
              {album.title}
            </h4>
            <p className="text-sm text-gray-400">
              {album.release_year ? `Year: ${album.release_year}` : "Unknown Year"}
            </p>
          </div>
        </Link>
      ))}
    </div>
  );
}
