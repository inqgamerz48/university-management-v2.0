"use client";

import { useState, useRef, type DragEvent } from "react";
import { UploadCloud, File, X } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

export function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
      e.dataTransfer.clearData();
    }
  };

  const handleFile = (selectedFile: File) => {
    if (file || uploadProgress > 0) {
      toast({
        title: "Upload in Progress",
        description: "Please wait for the current upload to finish.",
        variant: "destructive",
      });
      return;
    }

    setFile(selectedFile);
    setUploadProgress(0);

    // Simulate upload
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          toast({
            title: "Upload Successful",
            description: `${selectedFile.name} has been uploaded.`,
          });
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleRemoveFile = () => {
    setFile(null);
    setUploadProgress(0);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full space-y-4">
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={cn(
          "flex w-full flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 text-center transition-colors",
          isDragging ? "border-primary bg-primary/10" : "border-border hover:border-primary/50"
        )}
      >
        <UploadCloud className="mb-4 h-12 w-12 text-muted-foreground" />
        <p className="mb-2 text-lg font-semibold">
          Drag & Drop your file here
        </p>
        <p className="mb-4 text-sm text-muted-foreground">
          or
        </p>
        <Button type="button" variant="outline" onClick={handleBrowseClick}>
          Browse Files
        </Button>
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          onChange={(e) => e.target.files && handleFile(e.target.files[0])}
        />
      </div>
      {file && (
        <div className="rounded-lg border p-4">
          <div className="flex items-center gap-4">
            <File className="h-8 w-8 text-primary" />
            <div className="flex-1">
              <p className="font-medium">{file.name}</p>
              <p className="text-sm text-muted-foreground">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            {uploadProgress < 100 && (
              <p className="text-sm font-semibold">{uploadProgress}%</p>
            )}
            {uploadProgress === 100 && (
              <Button variant="ghost" size="icon" onClick={handleRemoveFile}>
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
          {uploadProgress > 0 && (
            <Progress value={uploadProgress} className="mt-2 h-2" />
          )}
        </div>
      )}
    </div>
  );
}
